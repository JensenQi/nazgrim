#!/usr/bin/env bash
article_name=$1
cd ${article_name}

# 清理LaTeX临时日志
rm -rf *.aux
rm -rf *.log
rm -rf *.dvi
rm -rf *.toc
rm -rf *.synctex.gz
rm -rf body/*.aux
rm -rf body/*.log
rm -rf setup/*.aux
rm -rf setup/*.log

# 生成html
rm rm -rf html
mkdir -p html/${article_name}/${article_name}
cp main.pdf html
cd html
pdf2htmlEX --split-pages 1 --dest-dir ${article_name} --page-filename ${article_name}/part-%d.page main.pdf
mkdir pages
mv ${article_name}/${article_name}/* pages/
mv ${article_name}/main.html main.html
rm -rf ${article_name}
rm -rf main.pdf
