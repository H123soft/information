var currentCid = 1; // 当前分类 id
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据


$(function () {
    // 界面加载完成之后去加载新闻数据
    updateNewsData()

    // 首页分类切换
    $('.menu li').click(function () {
        // 取到指定分类的cid
        var clickCid = $(this).attr('data-cid');
        // 遍历所有的li 移除身上的选中效果
        $('.menu li').each(function () {
            $(this).removeClass('active')
        });
        // 给当前分类添加选中的状态
        $(this).addClass('active');
        // 如果点击的分类与当前分类不一致
        if (clickCid != currentCid) {
            // 记录当前分类id
            currentCid = clickCid

            // 重置分页参数
            cur_page = 1
            total_page = 1
            updateNewsData()
        }
    })

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100) {
            //  判断页数，去更新新闻数据
            if(!data_querying){
                data_querying=true
                //如果当前页数如果小于总页数，就去加载数据
                if(cur_page<total_page){
                    cur_page += 1
                    // 去加载数据
                    updateNewsData()
                }
            }
        }
    })
})

function updateNewsData() {
    //  更新新闻数据
    var params = {
        "cid": currentCid,
        "page": cur_page

    };
    $.get("/news_list", params, function (resp) {
        // 数据加载完毕，设置【正在加载数据】的变量为flase，代表当前没有在加载数据
        data_querying=false
        if (resp.errno = "0") {
            // 给总页数赋值
            total_page = resp.data.total_page
            // 代表请求成功
            // 清除已有数据
            if(cur_page==1){
                $('.list_con').html("")
            }


            // 添加请求成功之后返回的数据
            // 显示数据
            for (var i = 0; i < resp.data.news_dict_li.length; i++) {
                var news = resp.data.news_dict_li[i]
                var content = '<li>'
                content += '<a href="/news/'+news.id+'" class="news_pic fl"><img src="' + news.index_image_url + '?imageView2/1/w/170/h/170"></a>'
                content += '<a href="/news/'+news.id+'" class="news_title fl">' + news.title + '</a>'
                content += '<a href="/news/'+news.id+'" class="news_detail fl">' + news.digest + '</a>'
                content += '<div class="author_info fl">'
                content += '<div class="source fl">来源：' + news.source + '</div>'
                content += '<div class="time fl">' + news.create_time + '</div>'
                content += '</div>'
                content += '</li>'
                $(".list_con").append(content)


            }
        }else
            {
                //代表请求失败
                alert(resp.errmsg)
            }

        }
    )

}
