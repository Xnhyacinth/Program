import torch
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModel, AdamW
import os
from utils import *
os.environ['CUDA_VISIBLE_DEVICES'] = '5'


def load_data(corpus_path, query_path, label_path):
    with open(corpus_path, 'r') as f:
        data = f.readlines()
    # format: {pid: passage}
    passages = {}
    for d in data:
        pid, passage = d.split('\t')
        passages[pid] = passage

    with open(query_path, 'r') as f:
        data = f.readlines()
    # format: {qid, query}
    queries = {}
    for d in data:
        qid, query = d.split('\t')
        queries[qid] = query

    # format: (qid, 0, pid, rating)
    with open(label_path, 'r') as f:
        data = f.readlines()
    labels = {}
    # format: {(qid, pid): rating}
    # 全都是相关的，所以rating都是1
    for d in data:
        qid, _, pid, rating = d.split('\t')
        labels[(qid, pid)] = int(rating)

    return passages, queries, labels


class PassageRerankDataset(Dataset):
    def __init__(self, passages, queries, labels, tokenizer, max_len, is_train=True):
        self.passages = passages
        self.queries = queries
        self.labels = labels
        if is_train:
            self.data = [(query, passage, self.labels.get((query, passage), 0))
                         for query in queries.keys() for passage in passages.keys()]
        else:
            self.data = [(query, passage, label)
                         for (query, passage), label in self.labels.items()]
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        qid, pid, label = self.data[idx]
        query = str(self.queries[qid])
        passage = str(self.passages[pid])
        label = int(label)

        encoding = self.tokenizer(
            passage,
            query,
            add_special_tokens=True,
            max_length=self.max_len,
            return_tensors='pt',
            padding='max_length',
            truncation=True
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'token_type_ids': encoding['token_type_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'label': torch.tensor(label, dtype=torch.long),
            'qid': qid,
            'pid': pid
        }


class PassageRerankModel(torch.nn.Module):
    def __init__(self):
        super(PassageRerankModel, self).__init__()
        bert = 'bert-base-uncased'
        self.bert = AutoModel.from_pretrained(bert)
        self.dropout = nn.Dropout(0.2)
        if any(name in bert for name in ['large', 'Ubert']):
            dim = 1024
        elif '1.3B' in bert:
            dim = 2048
        else:
            dim = 768
        self.linear = nn.Linear(dim, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids, attention_mask=attention_mask)
        pooler_output = outputs['pooler_output'] #Only Embedding for [CLS] is required in classification
        dropout_output = self.dropout(pooler_output)
        linear_output: torch.Tensor = self.linear(dropout_output) #[B, 1]
        score = self.sigmoid(linear_output.squeeze(-1))
        return score #[B]


def eval(model, eval_loader, metric, device):
    model.eval()
    all_preds = []
    pids = {}
    for step, input in enumerate(tqdm(eval_loader)):
        input_ids: torch.Tensor = input['input_ids'].to(device)
        attention_mask: torch.Tensor = input['attention_mask'].to(device)

        score = model(input_ids, attention_mask)
        # 这里存它的相反数，方便argsort
        for i in range(len(input['qid'])):
            pids[i + step * len(input['qid'])] = input['pid'][i]
        pred = [(input['qid'][i], i + step * len(input['qid']), -score[i].item())
                for i in range(len(input['qid']))]
        all_preds.extend(pred)

    score = metric.get_ndcg(all_preds, pids)
    return score

SAVE_PATH =  os.path.join('model', 'bert-base')
if __name__ == '__main__':

    tokenizer = AutoTokenizer.from_pretrained('bert-large-uncased')
    max_len = 512

    passages, queries, labels = load_data(
        'sample/collection.sampled.tsv', 'sample/train_sample_queries.tsv', 'sample/train_sample_passv2_qrels.tsv')
    dataset = PassageRerankDataset(
        passages, queries, labels, tokenizer, max_len)
    train_loader = DataLoader(dataset, batch_size=32, shuffle=True)
    print('finish load train dataset')
    val_queries, val_labels = load_eval_dataset(
        'sample/val_2021_53_queries.tsv', 'sample/val_2021_passage_top100.txt')
    val_dataset = PassageRerankDataset(passages, val_queries, val_labels, tokenizer, max_len, False)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
    print('finish load eval dataset')
    metric = Metric()

    model = PassageRerankModel()
    optimizer = AdamW(model.parameters(), lr=1e-5)

    num_epochs = 5
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    criterion = nn.BCELoss(reduction='sum')
    best_score = 0
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0
        for batch in train_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            token_type_ids = batch['token_type_ids'].to(device)
            labels = batch['label'].to(device)

            optimizer.zero_grad()
            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, labels.float())
            total_loss += loss.item()

            loss.backward()
            optimizer.step()

        avg_loss = total_loss / len(train_loader)
        print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {avg_loss}')
        
        score = eval(model, val_loader, metric, device)
        if score > best_score:
            print(f'evaluation result:{score}')
            torch.save(model.state_dict(), os.path.join(SAVE_PATH, 'best.pt'))
            best_score = score
            print(f'state dict saved to {SAVE_PATH}')
