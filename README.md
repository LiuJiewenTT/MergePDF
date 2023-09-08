# MergePDF

## 介绍

这是一个对已有库的封装的脚本，专注于PDF合并，提供一些操作选项和优化操作的可能。

## 说明

可用选项：

-o
: 选择输出文件名（路径仅限相对路径）。未指定情况下，使用第一个名称添加".out"于名称与扩展名之间。

-f
: 指定其后的字符串表示的是文件。同名文件夹和文件同时存在的情况下默认为缺省此选项。

-d
: 指定其后的字符串表示的是文件夹。此时会按照一定顺序把文件夹下的PDF文件加入列表。

--NoAssumption-FileType
: 对未指定字符串不进行猜测，如果存在为明确指定类型的字符串，提示并终止。