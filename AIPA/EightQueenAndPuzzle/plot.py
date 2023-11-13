import matplotlib.pyplot as plt

# 绘制性能曲线
def plot_performance_curve(scores_ed, scores_eq):
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False
    plt.figure(figsize=(10, 5))
    x = [0, 1, 2, 3]
    # plt.subplot(1, 2, 1)
    # plt.plot(sum(costs[:max_attempts]) / max_attempts, label='Hill Climbing')
    # plt.plot(sum(costs[max_attempts:]) / max_attempts, label='Random Restart Hill Climbing')
    # plt.plot(sum(costs_first_choice) / max_attempts, label='First Choice Hill Climbing')
    # plt.plot(sum(costs_simulated_annealing) / max_attempts, label='Simulated Annealing')
    plt.plot(scores_ed, label='八数码')
    # plt.plot(scores_eq, label='八皇后')
    plt.xticks(x, ['最陡上升爬山法', '首选爬山法', '随机重启爬山法', '模拟退火算法'])
    plt.xlabel("方法")
    plt.ylabel("成功率")
    plt.title("四种方法查找成功率的比较")
    
    plt.plot(scores_eq, label='八皇后')
    for i, prob in enumerate(scores_eq):
        if prob > 0.001:
            plt.text(x[i], prob, f'{prob:.3f}', ha='center', va='bottom')
    for i, prob in enumerate(scores_ed):
        if prob > 0.001:
            plt.text(x[i], prob, f'{prob:.3f}', ha='center', va='bottom')
    # plt.subplot(1, 2, 2)
    # a = [sum(success_rates[:max_attempts]) / max_attempts]
    # a.append(sum(success_rates[max_attempts:]) / max_attempts)
    # a.append(sum(success_rates_first_choice) / max_attempts)
    # a.append(sum(success_rates_simulated_annealing) / max_attempts)
    # plt.plot(a, label='Simulated Annealing')
    # plt.plot(sum(success_rates[:max_attempts]) / max_attempts, label='Hill Climbing')
    # plt.plot(sum(success_rates[max_attempts:]) / max_attempts, label='Random Restart Hill Climbing')
    # plt.plot(sum(success_rates_first_choice) / max_attempts, label='First Choice Hill Climbing')
    # plt.plot(sum(success_rates_simulated_annealing) / max_attempts, label='Simulated Annealing')
    plt.legend()
    # plt.xlabel("Attempts")
    # plt.ylabel("Success Rate")
    # plt.title(f"Success Rate vs. Attempts (Max Attempts = {max_attempts})")
    plt.savefig('a.png')
    
# 绘制性能曲线
def plot_time(times_ed, times_eq):
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus']=False
    plt.figure(figsize=(10, 5))
    x = [0, 1, 2, 3]
    # plt.subplot(1, 2, 1)
    # plt.plot(sum(costs[:max_attempts]) / max_attempts, label='Hill Climbing')
    # plt.plot(sum(costs[max_attempts:]) / max_attempts, label='Random Restart Hill Climbing')
    # plt.plot(sum(costs_first_choice) / max_attempts, label='First Choice Hill Climbing')
    # plt.plot(sum(costs_simulated_annealing) / max_attempts, label='Simulated Annealing')
    plt.plot(times_ed, label='八数码')
    # plt.plot(scores_eq, label='八皇后')
    plt.xticks(x, ['最陡上升爬山法', '首选爬山法', '随机重启爬山法', '模拟退火算法'])
    plt.xlabel("方法")
    plt.ylabel("运行时间")
    plt.title("四种方法搜索耗散的比较")
    
    plt.plot(times_eq, label='八皇后')
    for i, prob in enumerate(times_eq):
        if prob > 0.001:
            plt.text(x[i], prob, f'{prob:.3f}', ha='center', va='bottom')
    for i, prob in enumerate(times_ed):
        if prob > 0.001:
            plt.text(x[i], prob, f'{prob:.3f}', ha='center', va='top')
    # plt.subplot(1, 2, 2)
    # a = [sum(success_rates[:max_attempts]) / max_attempts]
    # a.append(sum(success_rates[max_attempts:]) / max_attempts)
    # a.append(sum(success_rates_first_choice) / max_attempts)
    # a.append(sum(success_rates_simulated_annealing) / max_attempts)
    # plt.plot(a, label='Simulated Annealing')
    # plt.plot(sum(success_rates[:max_attempts]) / max_attempts, label='Hill Climbing')
    # plt.plot(sum(success_rates[max_attempts:]) / max_attempts, label='Random Restart Hill Climbing')
    # plt.plot(sum(success_rates_first_choice) / max_attempts, label='First Choice Hill Climbing')
    # plt.plot(sum(success_rates_simulated_annealing) / max_attempts, label='Simulated Annealing')
    plt.legend()
    # plt.xlabel("Attempts")
    # plt.ylabel("Success Rate")
    # plt.title(f"Success Rate vs. Attempts (Max Attempts = {max_attempts})")
    plt.savefig('b.png')
    
plot_time([0.08510112762451172, 0.12096834582, 1868.188981294632, 4508.823776245117], [8.560140371322632, 9.35342264175415, 1351.625123500824, 3887.748220205307])