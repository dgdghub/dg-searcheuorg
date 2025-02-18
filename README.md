# hello
https://github.com/dgdghub/dg-searcheuorg.git

# touch env
```
touch .env
vi .env
sudo chmod 777 .env
```
```
# 安装
sudo pip install -r requirements.txt --break-system-packages
```
```
# 启动
pm2 start app.py --name euorg-app --interpreter python3 --no-autorestart
```
or
```
pm2 start gen_app.py --name euorg-app --interpreter python3
```
# 提示词
输入一个字符串参数，这个参数包含26个小写英文字母和0-9的数字；要求随机生成新的字符串；生成的新字符串长度随机，最少4位，最多8位； 不能重复生成，生成的新字符串是唯一的，也就是说遇到已经生成过多字符串要跳过；新生成的字符串可能是纯字母也可能是纯数字，也可能是字母和数字的组合；新生成的字符串看上去像是人类常用的单词的，而不能像乱码一样毫无意义，因为我要拿这个字符串用作域名；如果新生成的字符串是字母和数字的混合，那么所包含的数字只能出现在字符串首尾不能出现在中间，也就是说aabb22cc是不合适的，应为中间出现了22；如果所生成的字符串中有重叠数字，例如88,66,111,999这样，最多重叠5位, 例如555555,a5555555这种事不合法的，因为数字5出现的次数超过了5次；新生成的字符串中所包含的字母的重叠数量也不能超过5，例如aaaaaa22,999bbbbbbb这种字符串，第一个由于a的数量大于5了，第二个b的数量大于5了，所以这种是不合适的；新生成的这个字符串在passed.txt文件中不可以存在，用python完成