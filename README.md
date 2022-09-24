# findUnuseLocKey
找出iOS项目中多语言Localizable.strings中无用的key

## 使用: 
参数说明：
--fl=英文多语言文件地址
--fd=项目根目录
--delete= 是否直接删除无用的keys(默认为false)

```ruby
python findUnuseLocKey.py --fl=/Users/jinfu/Desktop/python练习/banggood/en.lproj/Localizable.strings --fd=/Users/jinfu/Desktop/python练习/banggood --delete=1
```

当前目录下生成文件：unuseLocKeys.txt(未使用到的key会生成个文件输出)
