import { SvelteComponent, init, safe_not_equal, create_slot, element, space, claim_element, children, get_svelte_dataset, claim_space, detach, attr, toggle_class, insert_hydration, append_hydration, listen, update_slot_base, get_all_dirty_from_scope, get_slot_changes, transition_in, transition_out, createEventDispatcher, onMount, binding_callbacks, assign, create_component, empty, claim_component, mount_component, get_spread_update, get_spread_object, group_outros, check_outros, destroy_component, bind, add_flush_callback } from "../../../svelte/svelte.js";
import "../../../svelte/svelte-submodules.js";
import { S as Static, t as Index$1 } from "./2.BUksOkfw.js";
function create_fragment$1(ctx) {
  let div2;
  let button;
  let textContent = `<div class="chevron svelte-y4v1h1"><span class="chevron-left svelte-y4v1h1"></span></div>`;
  let t;
  let div1;
  let div2_style_value;
  let current;
  let mounted;
  let dispose;
  const default_slot_template = (
    /*#slots*/
    ctx[10].default
  );
  const default_slot = create_slot(
    default_slot_template,
    ctx,
    /*$$scope*/
    ctx[9],
    null
  );
  return {
    c() {
      div2 = element("div");
      button = element("button");
      button.innerHTML = textContent;
      t = space();
      div1 = element("div");
      if (default_slot)
        default_slot.c();
      this.h();
    },
    l(nodes) {
      div2 = claim_element(nodes, "DIV", { class: true, style: true });
      var div2_nodes = children(div2);
      button = claim_element(div2_nodes, "BUTTON", {
        class: true,
        "aria-label": true,
        ["data-svelte-h"]: true
      });
      if (get_svelte_dataset(button) !== "svelte-k78zcg")
        button.innerHTML = textContent;
      t = claim_space(div2_nodes);
      div1 = claim_element(div2_nodes, "DIV", { class: true });
      var div1_nodes = children(div1);
      if (default_slot)
        default_slot.l(div1_nodes);
      div1_nodes.forEach(detach);
      div2_nodes.forEach(detach);
      this.h();
    },
    h() {
      attr(button, "class", "toggle-button svelte-y4v1h1");
      attr(button, "aria-label", "Toggle Sidebar");
      attr(div1, "class", "sidebar-content svelte-y4v1h1");
      attr(div2, "class", "sidebar svelte-y4v1h1");
      attr(div2, "style", div2_style_value = "width: " + /*width_css*/
      ctx[5] + "; " + /*position*/
      ctx[0] + ": calc(" + /*width_css*/
      ctx[5] + " * -1)");
      toggle_class(
        div2,
        "open",
        /*_open*/
        ctx[1]
      );
      toggle_class(
        div2,
        "right",
        /*position*/
        ctx[0] === "right"
      );
      toggle_class(
        div2,
        "reduce-motion",
        /*prefersReducedMotion*/
        ctx[3]
      );
    },
    m(target, anchor) {
      insert_hydration(target, div2, anchor);
      append_hydration(div2, button);
      append_hydration(div2, t);
      append_hydration(div2, div1);
      if (default_slot) {
        default_slot.m(div1, null);
      }
      ctx[12](div2);
      current = true;
      if (!mounted) {
        dispose = listen(
          button,
          "click",
          /*click_handler*/
          ctx[11]
        );
        mounted = true;
      }
    },
    p(ctx2, [dirty]) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & /*$$scope*/
        512)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            /*$$scope*/
            ctx2[9],
            !current ? get_all_dirty_from_scope(
              /*$$scope*/
              ctx2[9]
            ) : get_slot_changes(
              default_slot_template,
              /*$$scope*/
              ctx2[9],
              dirty,
              null
            ),
            null
          );
        }
      }
      if (!current || dirty & /*position*/
      1 && div2_style_value !== (div2_style_value = "width: " + /*width_css*/
      ctx2[5] + "; " + /*position*/
      ctx2[0] + ": calc(" + /*width_css*/
      ctx2[5] + " * -1)")) {
        attr(div2, "style", div2_style_value);
      }
      if (!current || dirty & /*_open*/
      2) {
        toggle_class(
          div2,
          "open",
          /*_open*/
          ctx2[1]
        );
      }
      if (!current || dirty & /*position*/
      1) {
        toggle_class(
          div2,
          "right",
          /*position*/
          ctx2[0] === "right"
        );
      }
      if (!current || dirty & /*prefersReducedMotion*/
      8) {
        toggle_class(
          div2,
          "reduce-motion",
          /*prefersReducedMotion*/
          ctx2[3]
        );
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (detaching) {
        detach(div2);
      }
      if (default_slot)
        default_slot.d(detaching);
      ctx[12](null);
      mounted = false;
      dispose();
    }
  };
}
function instance$1($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  const dispatch = createEventDispatcher();
  let { open = true } = $$props;
  let { width } = $$props;
  let { position = "left" } = $$props;
  let mounted = false;
  let _open = false;
  let sidebar_div;
  let overlap_amount = 0;
  let width_css = typeof width === "number" ? `${width}px` : width;
  let prefersReducedMotion;
  function check_overlap() {
    var _a;
    if (!sidebar_div.closest(".wrap"))
      return;
    const parent_rect = (_a = sidebar_div.closest(".wrap")) == null ? void 0 : _a.getBoundingClientRect();
    if (!parent_rect)
      return;
    const sidebar_rect = sidebar_div.getBoundingClientRect();
    const available_space = position === "left" ? parent_rect.left : window.innerWidth - parent_rect.right;
    overlap_amount = Math.max(0, sidebar_rect.width - available_space + 30);
  }
  onMount(() => {
    var _a;
    (_a = sidebar_div.closest(".wrap")) == null ? void 0 : _a.classList.add("sidebar-parent");
    check_overlap();
    window.addEventListener("resize", check_overlap);
    const update_parent_overlap = () => {
      document.documentElement.style.setProperty("--overlap-amount", `${overlap_amount}px`);
    };
    update_parent_overlap();
    $$invalidate(8, mounted = true);
    const mediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
    $$invalidate(3, prefersReducedMotion = mediaQuery.matches);
    const updateMotionPreference = (e) => {
      $$invalidate(3, prefersReducedMotion = e.matches);
    };
    mediaQuery.addEventListener("change", updateMotionPreference);
    return () => {
      window.removeEventListener("resize", check_overlap);
      mediaQuery.removeEventListener("change", updateMotionPreference);
    };
  });
  const click_handler = () => {
    $$invalidate(1, _open = !_open);
    if (_open) {
      dispatch("expand");
    } else {
      dispatch("collapse");
    }
  };
  function div2_binding($$value) {
    binding_callbacks[$$value ? "unshift" : "push"](() => {
      sidebar_div = $$value;
      $$invalidate(2, sidebar_div);
    });
  }
  $$self.$$set = ($$props2) => {
    if ("open" in $$props2)
      $$invalidate(6, open = $$props2.open);
    if ("width" in $$props2)
      $$invalidate(7, width = $$props2.width);
    if ("position" in $$props2)
      $$invalidate(0, position = $$props2.position);
    if ("$$scope" in $$props2)
      $$invalidate(9, $$scope = $$props2.$$scope);
  };
  $$self.$$.update = () => {
    if ($$self.$$.dirty & /*mounted, open*/
    320) {
      if (mounted)
        $$invalidate(1, _open = open);
    }
  };
  return [
    position,
    _open,
    sidebar_div,
    prefersReducedMotion,
    dispatch,
    width_css,
    open,
    width,
    mounted,
    $$scope,
    slots,
    click_handler,
    div2_binding
  ];
}
class Sidebar extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance$1, create_fragment$1, safe_not_equal, { open: 6, width: 7, position: 0 });
  }
}
function create_if_block(ctx) {
  let sidebar;
  let updating_open;
  let updating_position;
  let current;
  function sidebar_open_binding(value) {
    ctx[7](value);
  }
  function sidebar_position_binding(value) {
    ctx[8](value);
  }
  let sidebar_props = {
    width: (
      /*width*/
      ctx[4]
    ),
    $$slots: { default: [create_default_slot] },
    $$scope: { ctx }
  };
  if (
    /*open*/
    ctx[0] !== void 0
  ) {
    sidebar_props.open = /*open*/
    ctx[0];
  }
  if (
    /*position*/
    ctx[1] !== void 0
  ) {
    sidebar_props.position = /*position*/
    ctx[1];
  }
  sidebar = new Sidebar({ props: sidebar_props });
  binding_callbacks.push(() => bind(sidebar, "open", sidebar_open_binding));
  binding_callbacks.push(() => bind(sidebar, "position", sidebar_position_binding));
  sidebar.$on(
    "expand",
    /*expand_handler*/
    ctx[9]
  );
  sidebar.$on(
    "collapse",
    /*collapse_handler*/
    ctx[10]
  );
  return {
    c() {
      create_component(sidebar.$$.fragment);
    },
    l(nodes) {
      claim_component(sidebar.$$.fragment, nodes);
    },
    m(target, anchor) {
      mount_component(sidebar, target, anchor);
      current = true;
    },
    p(ctx2, dirty) {
      const sidebar_changes = {};
      if (dirty & /*width*/
      16)
        sidebar_changes.width = /*width*/
        ctx2[4];
      if (dirty & /*$$scope*/
      2048) {
        sidebar_changes.$$scope = { dirty, ctx: ctx2 };
      }
      if (!updating_open && dirty & /*open*/
      1) {
        updating_open = true;
        sidebar_changes.open = /*open*/
        ctx2[0];
        add_flush_callback(() => updating_open = false);
      }
      if (!updating_position && dirty & /*position*/
      2) {
        updating_position = true;
        sidebar_changes.position = /*position*/
        ctx2[1];
        add_flush_callback(() => updating_position = false);
      }
      sidebar.$set(sidebar_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(sidebar.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(sidebar.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(sidebar, detaching);
    }
  };
}
function create_default_slot_1(ctx) {
  let current;
  const default_slot_template = (
    /*#slots*/
    ctx[6].default
  );
  const default_slot = create_slot(
    default_slot_template,
    ctx,
    /*$$scope*/
    ctx[11],
    null
  );
  return {
    c() {
      if (default_slot)
        default_slot.c();
    },
    l(nodes) {
      if (default_slot)
        default_slot.l(nodes);
    },
    m(target, anchor) {
      if (default_slot) {
        default_slot.m(target, anchor);
      }
      current = true;
    },
    p(ctx2, dirty) {
      if (default_slot) {
        if (default_slot.p && (!current || dirty & /*$$scope*/
        2048)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx2,
            /*$$scope*/
            ctx2[11],
            !current ? get_all_dirty_from_scope(
              /*$$scope*/
              ctx2[11]
            ) : get_slot_changes(
              default_slot_template,
              /*$$scope*/
              ctx2[11],
              dirty,
              null
            ),
            null
          );
        }
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(default_slot, local);
      current = true;
    },
    o(local) {
      transition_out(default_slot, local);
      current = false;
    },
    d(detaching) {
      if (default_slot)
        default_slot.d(detaching);
    }
  };
}
function create_default_slot(ctx) {
  let column;
  let current;
  column = new Index$1({
    props: {
      $$slots: { default: [create_default_slot_1] },
      $$scope: { ctx }
    }
  });
  return {
    c() {
      create_component(column.$$.fragment);
    },
    l(nodes) {
      claim_component(column.$$.fragment, nodes);
    },
    m(target, anchor) {
      mount_component(column, target, anchor);
      current = true;
    },
    p(ctx2, dirty) {
      const column_changes = {};
      if (dirty & /*$$scope*/
      2048) {
        column_changes.$$scope = { dirty, ctx: ctx2 };
      }
      column.$set(column_changes);
    },
    i(local) {
      if (current)
        return;
      transition_in(column.$$.fragment, local);
      current = true;
    },
    o(local) {
      transition_out(column.$$.fragment, local);
      current = false;
    },
    d(detaching) {
      destroy_component(column, detaching);
    }
  };
}
function create_fragment(ctx) {
  let statustracker;
  let t;
  let if_block_anchor;
  let current;
  const statustracker_spread_levels = [
    { autoscroll: (
      /*gradio*/
      ctx[3].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      ctx[3].i18n
    ) },
    /*loading_status*/
    ctx[2]
  ];
  let statustracker_props = {};
  for (let i = 0; i < statustracker_spread_levels.length; i += 1) {
    statustracker_props = assign(statustracker_props, statustracker_spread_levels[i]);
  }
  statustracker = new Static({ props: statustracker_props });
  let if_block = (
    /*visible*/
    ctx[5] && create_if_block(ctx)
  );
  return {
    c() {
      create_component(statustracker.$$.fragment);
      t = space();
      if (if_block)
        if_block.c();
      if_block_anchor = empty();
    },
    l(nodes) {
      claim_component(statustracker.$$.fragment, nodes);
      t = claim_space(nodes);
      if (if_block)
        if_block.l(nodes);
      if_block_anchor = empty();
    },
    m(target, anchor) {
      mount_component(statustracker, target, anchor);
      insert_hydration(target, t, anchor);
      if (if_block)
        if_block.m(target, anchor);
      insert_hydration(target, if_block_anchor, anchor);
      current = true;
    },
    p(ctx2, [dirty]) {
      const statustracker_changes = dirty & /*gradio, loading_status*/
      12 ? get_spread_update(statustracker_spread_levels, [
        dirty & /*gradio*/
        8 && { autoscroll: (
          /*gradio*/
          ctx2[3].autoscroll
        ) },
        dirty & /*gradio*/
        8 && { i18n: (
          /*gradio*/
          ctx2[3].i18n
        ) },
        dirty & /*loading_status*/
        4 && get_spread_object(
          /*loading_status*/
          ctx2[2]
        )
      ]) : {};
      statustracker.$set(statustracker_changes);
      if (
        /*visible*/
        ctx2[5]
      ) {
        if (if_block) {
          if_block.p(ctx2, dirty);
          if (dirty & /*visible*/
          32) {
            transition_in(if_block, 1);
          }
        } else {
          if_block = create_if_block(ctx2);
          if_block.c();
          transition_in(if_block, 1);
          if_block.m(if_block_anchor.parentNode, if_block_anchor);
        }
      } else if (if_block) {
        group_outros();
        transition_out(if_block, 1, 1, () => {
          if_block = null;
        });
        check_outros();
      }
    },
    i(local) {
      if (current)
        return;
      transition_in(statustracker.$$.fragment, local);
      transition_in(if_block);
      current = true;
    },
    o(local) {
      transition_out(statustracker.$$.fragment, local);
      transition_out(if_block);
      current = false;
    },
    d(detaching) {
      if (detaching) {
        detach(t);
        detach(if_block_anchor);
      }
      destroy_component(statustracker, detaching);
      if (if_block)
        if_block.d(detaching);
    }
  };
}
function instance($$self, $$props, $$invalidate) {
  let { $$slots: slots = {}, $$scope } = $$props;
  let { open = true } = $$props;
  let { position = "left" } = $$props;
  let { loading_status } = $$props;
  let { gradio } = $$props;
  let { width } = $$props;
  let { visible = true } = $$props;
  function sidebar_open_binding(value) {
    open = value;
    $$invalidate(0, open);
  }
  function sidebar_position_binding(value) {
    position = value;
    $$invalidate(1, position);
  }
  const expand_handler = () => gradio.dispatch("expand");
  const collapse_handler = () => gradio.dispatch("collapse");
  $$self.$$set = ($$props2) => {
    if ("open" in $$props2)
      $$invalidate(0, open = $$props2.open);
    if ("position" in $$props2)
      $$invalidate(1, position = $$props2.position);
    if ("loading_status" in $$props2)
      $$invalidate(2, loading_status = $$props2.loading_status);
    if ("gradio" in $$props2)
      $$invalidate(3, gradio = $$props2.gradio);
    if ("width" in $$props2)
      $$invalidate(4, width = $$props2.width);
    if ("visible" in $$props2)
      $$invalidate(5, visible = $$props2.visible);
    if ("$$scope" in $$props2)
      $$invalidate(11, $$scope = $$props2.$$scope);
  };
  return [
    open,
    position,
    loading_status,
    gradio,
    width,
    visible,
    slots,
    sidebar_open_binding,
    sidebar_position_binding,
    expand_handler,
    collapse_handler,
    $$scope
  ];
}
class Index extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance, create_fragment, safe_not_equal, {
      open: 0,
      position: 1,
      loading_status: 2,
      gradio: 3,
      width: 4,
      visible: 5
    });
  }
}
export {
  Index as default
};
