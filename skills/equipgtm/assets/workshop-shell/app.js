// EquipGTM workshop shell: readable code tools and keyboard-accessible navigation.
(function () {
  function legacyCopy(text) {
    var field = document.createElement("textarea");
    field.value = text;
    field.setAttribute("readonly", "");
    field.style.cssText = "position:fixed;left:-9999px;top:0;font-size:16px";
    document.body.appendChild(field);
    var focused = document.activeElement;
    try {
      field.select();
      if (!document.execCommand("copy")) throw new Error("Copy unavailable");
    } finally {
      field.remove();
      if (focused && focused.focus) focused.focus({ preventScroll: true });
    }
  }

  function copyText(text) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(text).catch(function () { legacyCopy(text); });
    }
    return Promise.resolve().then(function () { legacyCopy(text); });
  }

  function addCopyButtons() {
    var seen = new Set();
    document.querySelectorAll(".content .codehilite, .content pre").forEach(function (el) {
      var target = el.closest(".codehilite") || el;
      if (seen.has(target)) return;
      seen.add(target);
      if (target.parentElement && target.parentElement.classList.contains("codewrap")) return;
      var wrap = document.createElement("div");
      wrap.className = "codewrap";
      target.parentNode.insertBefore(wrap, target);
      var toolbar = document.createElement("div");
      toolbar.className = "code-tools";
      var status = document.createElement("span");
      status.className = "copy-status";
      status.setAttribute("role", "status");
      var btn = document.createElement("button");
      btn.className = "copy-btn";
      btn.type = "button";
      btn.textContent = "Copy";
      btn.setAttribute("aria-label", "Copy code");
      toolbar.appendChild(status);
      toolbar.appendChild(btn);
      wrap.appendChild(toolbar);
      wrap.appendChild(target);
      var pre = target.matches("pre") ? target : target.querySelector("pre");
      if (pre) {
        pre.tabIndex = 0;
        pre.setAttribute("aria-label", "Code block; scroll to read long lines");
      }
      var resetTimer;
      btn.addEventListener("click", function () {
        clearTimeout(resetTimer);
        status.textContent = "";
        var code = target.querySelector("code") || pre || target;
        copyText(code.textContent.replace(/\n$/, "")).then(function () {
          btn.textContent = "Copied";
          btn.classList.add("copied");
          status.textContent = "Code copied.";
          resetTimer = setTimeout(function () {
            btn.textContent = "Copy";
            btn.classList.remove("copied");
            status.textContent = "";
          }, 2400);
        }).catch(function () {
          btn.textContent = "Copy";
          btn.classList.remove("copied");
          status.textContent = "Copy is unavailable. Select the code and copy it.";
        });
      });
    });
  }

  function addTableScrolling() {
    document.querySelectorAll(".content table").forEach(function (table) {
      if (table.parentElement.classList.contains("table-scroll")) return;
      var wrap = document.createElement("div");
      wrap.className = "table-scroll";
      wrap.tabIndex = 0;
      wrap.setAttribute("role", "region");
      wrap.setAttribute("aria-label", "Table; scroll to read all columns");
      table.parentNode.insertBefore(wrap, table);
      wrap.appendChild(table);
    });
  }

  function wireNav() {
    var toggle = document.getElementById("navToggle");
    var close = document.getElementById("sbCollapse");
    var sidebar = document.querySelector(".sidebar");
    var main = document.querySelector(".main");
    if (!toggle || !sidebar || !main) return;
    var mobile = window.matchMedia("(max-width: 900px)");
    var root = document.documentElement;
    var desktopCollapsed = root.classList.contains("nav-collapsed");
    root.classList.add("nav-enhanced");
    var mobileOpen = false;
    sidebar.id = "workshop-navigation";
    sidebar.setAttribute("role", "navigation");
    sidebar.setAttribute("aria-label", "Workshop");
    toggle.setAttribute("aria-controls", sidebar.id);
    main.id = "workshop-content";
    main.tabIndex = -1;
    var skip = document.createElement("a");
    skip.className = "skip-link";
    skip.href = "#workshop-content";
    skip.textContent = "Skip to workshop content";
    document.body.insertBefore(skip, document.body.firstChild);
    skip.addEventListener("click", function (event) {
      event.preventDefault();
      if (mobile.matches && mobileOpen) setExpanded(false);
      main.focus({ preventScroll: true });
      main.scrollIntoView();
    });
    sidebar.querySelectorAll("a.active, .sb-title.home").forEach(function (link) {
      link.setAttribute("aria-current", "page");
    });

    function update() {
      var expanded = mobile.matches ? mobileOpen : !desktopCollapsed;
      root.classList.toggle("nav-collapsed", !mobile.matches && desktopCollapsed);
      root.classList.toggle("nav-open", mobile.matches && mobileOpen);
      toggle.setAttribute("aria-expanded", String(expanded));
      toggle.setAttribute("aria-label", (expanded ? "Close" : "Open") + " workshop navigation");
      if (close) close.textContent = mobile.matches ? "Close navigation" : "Hide navigation";
      if (!expanded && sidebar.contains(document.activeElement)) toggle.focus();
    }
    function setExpanded(expanded) {
      if (mobile.matches) {
        mobileOpen = expanded;
      } else {
        desktopCollapsed = !expanded;
        try { localStorage.setItem("navCollapsed", desktopCollapsed ? "1" : "0"); } catch (e) {}
      }
      update();
    }
    toggle.addEventListener("click", function () {
      var expanded = toggle.getAttribute("aria-expanded") === "true";
      setExpanded(!expanded);
      if (!expanded && mobile.matches) {
        var first = sidebar.querySelector("button, a[href]");
        if (first) first.focus();
      }
    });
    if (close) close.addEventListener("click", function () {
      setExpanded(false);
      toggle.focus();
    });
    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && mobile.matches && mobileOpen) {
        setExpanded(false);
        toggle.focus();
      }
    });
    mobile.addEventListener("change", function () { mobileOpen = false; update(); });
    update();
    var topbar = document.querySelector(".topbar");
    if (topbar && window.ResizeObserver) {
      new ResizeObserver(function () {
        root.style.setProperty("--topbar-h", Math.ceil(topbar.getBoundingClientRect().height) + "px");
      }).observe(topbar);
    }
  }

  function init() { addCopyButtons(); addTableScrolling(); wireNav(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
