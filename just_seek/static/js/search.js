function a() {
    var f = $("#search-input").val();
    var e = $.trim(f);
    if (e !== "") {
        // window.location.href = "/search=" + encodeURI(e) + "&p=1"
        window.location.href = "/search=" + e
    } else {
        $("#search-input").attr("placeholder", "请在这里输入关键词进行搜索").focus()
    }
}

$("#search-btn").on("click", function () {
    a()
});
$(document).on("keydown", function (e) {
    if (e.keyCode == "13") {
        a()
    }
})