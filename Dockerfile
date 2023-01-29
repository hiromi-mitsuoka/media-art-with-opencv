# https://datawokagaku.com/startjupyternote/

# M1対策: https://qiita.com/silloi/items/739699337b9bf4883b3e
# FROM --platform=linux/amd64 ubuntu:latest

FROM ubuntu:latest

# NOTE: -y → Answer 'yes' to interactive (user inquiry)
RUN apt-get -y update && apt-get install -y \
    # composeの場合，Package 'sudo' has no installation candidate
    # sudo \
    wget \
    vim \
    # https://cocoinit23.com/docker-opencv-importerror-libgl-so-1-cannot-open-shared-object-file/
    libgl1-mesa-dev \
    # https://qiita.com/minarai/items/291a91c965789bb7223c
    gcc

# NOTE: /opt → 追加アプリケーション
# https://atmarkit.itmedia.co.jp/ait/articles/0108/07/news002.html
WORKDIR /opt

# https://repo.anaconda.com/archive
# NOTE: -b: 全てのオプションで`Yes`を選択
# NOTE: -p: インストール先のディクレトリ指定
# https://www.eureka-moments-blog.com/entry/2020/02/22/160931
RUN wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh && \
    sh /opt/Anaconda3-2022.05-Linux-x86_64.sh -b -p /opt/anaconda3  && \
    rm -f Anaconda3-2022.05-Linux-x86_64.sh

# NOTE: インストール先にパスを通す
ENV PATH /opt/anaconda3/bin:$PATH


# Install Python library
RUN pip install opencv-python
# install mypy: 静的型チェック
# https://ohke.hateblo.jp/entry/2020/10/03/230000
RUN pip install mypy
# install mlxtend: アソシエーション分析で利用
# http://rasbt.github.io/mlxtend/
RUN pip install mlxtend
# https://surpriselib.com/
RUN pip install scikit-surprise
# NOTE: pip → Tools for managing Python packages
RUN pip install --upgrade pip

WORKDIR /
RUN mkdir /work

# NOTE: user → root, password → Not used（Deprecated）
CMD ["jupyter", "lab", "--port=8888", "--ip=0.0.0.0", "--allow-root", "--LabApp.token=''"]