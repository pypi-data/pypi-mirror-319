const {
  SvelteComponent: u,
  append_hydration: f,
  attr: r,
  children: o,
  claim_element: h,
  claim_text: v,
  detach: c,
  element: g,
  init: m,
  insert_hydration: y,
  noop: d,
  safe_not_equal: b,
  set_data: w,
  text: E,
  toggle_class: _
} = window.__gradio__svelte__internal;
function q(n) {
  let e, a = (
    /*value*/
    (n[0] !== null ? (
      /*value*/
      n[0]
    ) : "") + ""
  ), i;
  return {
    c() {
      e = g("div"), i = E(a), this.h();
    },
    l(l) {
      e = h(l, "DIV", { class: !0 });
      var t = o(e);
      i = v(t, a), t.forEach(c), this.h();
    },
    h() {
      r(e, "class", "svelte-1gecy8w"), _(
        e,
        "table",
        /*type*/
        n[1] === "table"
      ), _(
        e,
        "gallery",
        /*type*/
        n[1] === "gallery"
      ), _(
        e,
        "selected",
        /*selected*/
        n[2]
      );
    },
    m(l, t) {
      y(l, e, t), f(e, i);
    },
    p(l, [t]) {
      t & /*value*/
      1 && a !== (a = /*value*/
      (l[0] !== null ? (
        /*value*/
        l[0]
      ) : "") + "") && w(i, a), t & /*type*/
      2 && _(
        e,
        "table",
        /*type*/
        l[1] === "table"
      ), t & /*type*/
      2 && _(
        e,
        "gallery",
        /*type*/
        l[1] === "gallery"
      ), t & /*selected*/
      4 && _(
        e,
        "selected",
        /*selected*/
        l[2]
      );
    },
    i: d,
    o: d,
    d(l) {
      l && c(e);
    }
  };
}
function C(n, e, a) {
  let { value: i } = e, { type: l } = e, { selected: t = !1 } = e;
  return n.$$set = (s) => {
    "value" in s && a(0, i = s.value), "type" in s && a(1, l = s.type), "selected" in s && a(2, t = s.selected);
  }, [i, l, t];
}
class D extends u {
  constructor(e) {
    super(), m(this, e, C, q, b, { value: 0, type: 1, selected: 2 });
  }
}
export {
  D as default
};
