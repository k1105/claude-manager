# GCPの仮想マシンで常時稼働させる

Claude Codeセッションをクラウド上で24時間稼働させる方法。

## 概要

ローカルPCではスリープや再起動で対話が止まる。GCP（Google Cloud Platform）のVM上で稼働させることで、常時応答可能になる。

## 手順

1. GCPでCompute Engineインスタンスを作成（e2-small程度で十分）
2. Node.js / Bun をインストール
3. Claude Codeをインストール・認証
4. `screen` や `tmux` でセッションを維持
5. `claude --channels plugin:discord@claude-plugins-official` で起動

## 注意

- APIの利用料が発生する
- VMの月額費用も発生する（e2-small: 約$15/月程度）
- セッションが切れた場合の自動復旧スクリプトを組むとより安定する
