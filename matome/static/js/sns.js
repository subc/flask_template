/* DOMの読み込み完了後に処理 */
if (window.addEventListener) {
    window.addEventListener("load", shareButtonReadSyncer, false);
} else {
    window.attachEvent("onload", shareButtonReadSyncer);
}

/* シェアボタンを読み込む関数 */
function shareButtonReadSyncer() {
// 遅延ロードする場合は次の行と、終わりの方にある行のコメント(//)を外す
    setTimeout(function () {
        // はてなブックマーク
        var scriptTag = document.createElement("script");
        scriptTag.type = "text/javascript";
        scriptTag.src = "https://b.st-hatena.com/js/bookmark_button.js";
        scriptTag.async = true;
        document.getElementsByTagName("head")[0].appendChild(scriptTag);

    }, 2000);	//ページを開いて5秒後(5,000ミリ秒後)にシェアボタンを読み込む
}