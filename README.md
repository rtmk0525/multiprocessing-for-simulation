# multiprocessing-for-simulation

$N$ 個のプロセスを $M$ 枚のGPUに割り振り、各プロセスが終わり次第次のプロセスを起動するサンプルコード

## 想定状況
- $N$ 個の数値実験タスクを終わらせたい。使用可能なGPUは $M$ 枚あるが、 $i$ 番目のGPUの同時起動可能なタスク数はメモリの関係で $N_i$ までである。そこで、GPUが空き次第タスクを割り当てることで逐次的に $N$ 個のタスクを終わらせたい。

## 動作確認手順

1. git clone
2. python仮想環境下で```pip install -r requirements.txt```
3. 以下の動作確認例のように入力

## 動作確認例

1. - 入力: ```python multi-run.py -c exp-1 -d 0 1 0 1 -check false```
      - ```-c KEY```により、```KEY```に部分一致する実験条件ファイル名を検索する。今回はexp-1-1.yaml, exp-1-2.yaml, exp-1-3.yaml（ $N=3$ ）
      - ```-d N_0 N_1 N_2 N_3```により、GPUに割り当てる同時起動タスク上限を指定する。今回は $M=4$ 枚のGPUのうち、GPU1, GPU3にタスクを1つずつ割り当てる（ $N_1=1, N_3=1$ ）
      - 各GPUで```python run.py -c CONFIG_FILE```が実行される
   - 実行ログの例:
        ```
        Start the process with configs/exp-1/exp-1-2.yaml
        Start the process with configs/exp-1/exp-1-1.yaml
        The process finished: python run.py -c configs/exp-1/exp-1-2.yaml [1/3]
        Start the process with configs/exp-1/exp-1-3.yaml
        The process finished: python run.py -c configs/exp-1/exp-1-1.yaml [2/3]
        The process finished: python run.py -c configs/exp-1/exp-1-3.yaml [3/3]
        ```
        - GPU2枚にプロセスが1つずつ割り当てられる(1,2行目)
        - 1つ目のプロセスが終了した直後(3行目)、3つ目のプロセスが起動(4行目)
        - 残りのプロセスが終了(5,6行目)
   - 計算結果: resultsに出力
2. - 入力: ```python multi-run.py -c "exp-(2|3)-1-\d*" -gpu false -d 3 -check false```
      - ```-c KEY```で正規表現を利用。今回はexp-2-1-1.yaml, exp-2-1-2.yaml, exp-3-1-1.yaml, exp-3-1-2.yaml（ $N=4$ ）
      - ```-gpu false```によりCPU上での実行を指定
      - ```-d 3```により、CPUに割り当てられる同時起動タスク上限を指定（ $M_0=3$ ）
   - 実行ログの例:
        ```
        Start the process with configs/exp-3/exp-3-1-2.yaml
        Start the process with configs/exp-2/exp-2-1-2.yaml
        Start the process with configs/exp-3/exp-3-1-1.yaml
        The process finished: python run.py -c configs/exp-2/exp-2-1-2.yaml [1/4]
        Start the process with configs/exp-2/exp-2-1-1.yaml
        The process finished: python run.py -c configs/exp-2/exp-2-1-1.yaml [2/4]
        The process finished: python run.py -c configs/exp-3/exp-3-1-2.yaml [3/4]
        The process finished: python run.py -c configs/exp-3/exp-3-1-1.yaml [4/4]
        ```
        - 最初に3つのプロセスが起動(1-3行目)
        - 1つ目のプロセスが終了した直後(4行目)、4つ目のプロセスが起動(5行目)
        - 残りのプロセスが終了(6-8行目)
   - 計算結果: resultsに出力

## 使用例
- 実行したい数値計算の実験条件をconfigsに、コードをmodelsに入れる
- 入力形式を変える際はmulti-run.py, run.py, src/multi_run_preprocesses.py, src/run_preprocesses.pyなどを適宜書き換える
