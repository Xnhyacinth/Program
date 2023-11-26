<!--
 * Copyright (c) 2023 by Huanxuan Liao, huanxuanliao@gmail.com, All Rights Reserved. 
 * @Author: Xnhyacinth, Xnhyacinth@qq.com
 * @Date: 2023-11-26 16:25:40
-->
# Language Model
Comparison of perplexity in language models utilizing feedforward neural networks, recurrent neural networks, and self-attention mechanism networks.

data: [https://data.statmt.org/news-crawl/zh/](https://data.statmt.org/news-crawl/zh/), the last 1000 sentences are designated as the validation set, while the remainder serves as the training set.
## 📁 Folder

```bash
├──data # train.txt test.txt
├──scripts # some scripts for examples
├──data.py # process data
├──get_data.py # split data
├──FNN_LM.py # FFN for LM
├──LM.py # RNN & LSTM & SAS for LM
├──utils.py # Logging
```