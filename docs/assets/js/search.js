// サイト内検索（クライアント側全文検索）
// search.json（Jekyll 生成のインデックス）を fetch し、
// タイトル・本文・タグへの部分一致で絞り込んで結果を表示する。
(function () {
  var input = document.getElementById("site-search-input");
  var results = document.getElementById("site-search-results");
  var indexUrl = window.PORTAL_SEARCH_INDEX_URL;
  if (!input || !results || !indexUrl) return;

  var pages = null;
  var failed = false;

  function el(tag, text) {
    var node = document.createElement(tag);
    if (text != null) node.textContent = text;
    return node;
  }

  function snippet(content, query) {
    var idx = content.toLowerCase().indexOf(query.toLowerCase());
    if (idx < 0) return content.slice(0, 120);
    var start = Math.max(0, idx - 40);
    var end = Math.min(content.length, idx + query.length + 80);
    return (start > 0 ? "…" : "") +
      content.slice(start, end) +
      (end < content.length ? "…" : "");
  }

  function render() {
    results.textContent = "";
    var query = input.value.trim();
    if (!query || !pages) return;
    var q = query.toLowerCase();

    var hits = pages.filter(function (p) {
      var tags = Array.isArray(p.tags) ? p.tags.join(" ") : (p.tags || "");
      return (p.title || "").toLowerCase().indexOf(q) >= 0 ||
        (p.content || "").toLowerCase().indexOf(q) >= 0 ||
        tags.toLowerCase().indexOf(q) >= 0;
    }).slice(0, 20);

    if (hits.length === 0) {
      results.appendChild(el("li", "「" + query + "」に一致するページはありません。"));
      return;
    }

    hits.forEach(function (p) {
      var li = el("li");
      li.style.marginBottom = "12px";
      var a = el("a", p.title || p.url);
      a.setAttribute("href", p.url);
      li.appendChild(a);

      var meta = "";
      var tagStr = Array.isArray(p.tags) ? p.tags.join(", ") : (p.tags || "");
      if (p.date) meta += "　" + p.date;
      if (tagStr) meta += "　タグ: " + tagStr;
      if (meta) {
        var small = el("small", meta);
        small.style.color = "#666";
        li.appendChild(small);
      }

      li.appendChild(el("br"));
      li.appendChild(el("span", snippet(p.content || "", query)));
      results.appendChild(li);
    });
  }

  function ensureIndex() {
    if (pages || failed) return;
    fetch(indexUrl)
      .then(function (res) { return res.json(); })
      .then(function (data) { pages = data; render(); })
      .catch(function () {
        failed = true;
        results.textContent = "検索インデックス（search.json）の読み込みに失敗しました。";
      });
  }

  input.addEventListener("focus", ensureIndex);
  input.addEventListener("input", function () {
    ensureIndex();
    render();
  });
})();
