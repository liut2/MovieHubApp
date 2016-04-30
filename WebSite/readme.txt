几点小的注意事项

1. 现在carousel 和登录的modal可以work了，然后我会接着优化modal, 你可以把之前写的card嵌套在carousel里头了。
2. 之所以之前有的css和js不起作用是因为没有正确的link file。对于css file我们只要在head里头link就好了，
但注意因为css文件是放在css directory里头的，所以需要css/xxx.css。另外我觉得一个general style是css的
代码尽量不要放在html里头，一旦html复杂之后很难看清html structure，对于每一个html，还是单独link一个与之
对应的css文件比较好。同样对于js file, 我们也需要列出来path, 比如js/xxx.js。一般来说，如果是我们引用的外部js
,比如jquery, 我们可以也在head link，如果是我们自己写的js file， 比如carousel.js, modal.js， 那么一般都在
body里头的最后link, 而且和css一样，最好所有的js都写在单独的文件里，方便以后modularity。例子可以参考carousel.js, modal.js
3. 开始学习一下jinja2 templating system，这样以后可以复用code。
