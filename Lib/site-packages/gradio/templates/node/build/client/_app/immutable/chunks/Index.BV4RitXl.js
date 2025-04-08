import { SvelteComponent, init, safe_not_equal, create_slot, element, space, claim_element, children, detach, claim_space, attr, toggle_class, insert_hydration, append_hydration, listen, is_function, update_slot_base, get_all_dirty_from_scope, get_slot_changes, transition_in, transition_out, text, claim_text, set_data, empty, get_svelte_dataset, run_all, noop, ensure_array_like, destroy_each } from "../../../svelte/svelte.js";
import "../../../svelte/svelte-submodules.js";
function get_each_context(ctx, list, i) {
  const child_ctx = ctx.slice();
  child_ctx[16] = list[i];
  return child_ctx;
}
function create_if_block_3(ctx) {
  let div;
  let span;
  let t0;
  let t1;
  let t2;
  let t3;
  return {
    c() {
      div = element("div");
      span = element("span");
      t0 = text(
        /*component_type*/
        ctx[2]
      );
      t1 = text(":");
      t2 = text(" ");
      t3 = text(
        /*var_name*/
        ctx[3]
      );
      this.h();
    },
    l(nodes) {
      div = claim_element(nodes, "DIV", { class: true });
      var div_nodes = children(div);
      span = claim_element(div_nodes, "SPAN", { class: true });
      var span_nodes = children(span);
      t0 = claim_text(
        span_nodes,
        /*component_type*/
        ctx[2]
      );
      t1 = claim_text(span_nodes, ":");
      span_nodes.forEach(detach);
      t2 = claim_text(div_nodes, " ");
      t3 = claim_text(
        div_nodes,
        /*var_name*/
        ctx[3]
      );
      div_nodes.forEach(detach);
      this.h();
    },
    h() {
      attr(span, "class", "svelte-1ccw3kh");
      attr(div, "class", "component-name svelte-1ccw3kh");
    },
    m(target, anchor) {
      insert_hydration(target, div, anchor);
      append_hydration(div, span);
      append_hydration(span, t0);
      append_hydration(span, t1);
      append_hydration(div, t2);
      append_hydration(div, t3);
    },
    p(ctx2, dirty) {
      if (dirty & /*component_type*/
      4)
        set_data(
          t0,
          /*component_type*/
          ctx2[2]
        );
      if (dirty & /*var_name*/
      8)
        set_data(
          t3,
          /*var_name*/
          ctx2[3]
        );
    },
    d(detaching) {
      if (detaching) {
        detach(div);
      }
    }
  };
}
function create_else_block(ctx) {
  let button0;
  let textContent = "+";
  let t1;
  let button1;
  let textContent_1 = "+";
  let t3;
  let button2;
  let textContent_2 = "+";
  let t5;
  let button3;
  let textContent_3 = "+";
  let t7;
  let if_block_anchor;
  let mounted;
  let dispose;
  let if_block = !/*is_container*/
  ctx[1] && create_if_block_2(ctx);
  return {
    c() {
      button0 = element("button");
      button0.textContent = textContent;
      t1 = space();
      button1 = element("button");
      button1.textContent = textContent_1;
      t3 = space();
      button2 = element("button");
      button2.textContent = textContent_2;
      t5 = space();
      button3 = element("button");
      button3.textContent = textContent_3;
      t7 = space();
      if (if_block)
        if_block.c();
      if_block_anchor = empty();
      this.h();
    },
    l(nodes) {
      button0 = claim_element(nodes, "BUTTON", { class: true, ["data-svelte-h"]: true });
      if (get_svelte_dataset(button0) !== "svelte-9vgc4e")
        button0.textContent = textContent;
      t1 = claim_space(nodes);
      button1 = claim_element(nodes, "BUTTON", { class: true, ["data-svelte-h"]: true });
      if (get_svelte_dataset(button1) !== "svelte-pewocm")
        button1.textContent = textContent_1;
      t3 = claim_space(nodes);
      button2 = claim_element(nodes, "BUTTON", { class: true, ["data-svelte-h"]: true });
      if (get_svelte_dataset(button2) !== "svelte-4vsur8")
        button2.textContent = textContent_2;
      t5 = claim_space(nodes);
      button3 = claim_element(nodes, "BUTTON", { class: true, ["data-svelte-h"]: true });
      if (get_svelte_dataset(button3) !== "svelte-c945mq")
        button3.textContent = textContent_3;
      t7 = claim_space(nodes);
      if (if_block)
        if_block.l(nodes);
      if_block_anchor = empty();
      this.h();
    },
    h() {
      attr(button0, "class", "add up svelte-1ccw3kh");
      attr(button1, "class", "add left svelte-1ccw3kh");
      attr(button2, "class", "add right svelte-1ccw3kh");
      attr(button3, "class", "add down svelte-1ccw3kh");
    },
    m(target, anchor) {
      insert_hydration(target, button0, anchor);
      insert_hydration(target, t1, anchor);
      insert_hydration(target, button1, anchor);
      insert_hydration(target, t3, anchor);
      insert_hydration(target, button2, anchor);
      insert_hydration(target, t5, anchor);
      insert_hydration(target, button3, anchor);
      insert_hydration(target, t7, anchor);
      if (if_block)
        if_block.m(target, anchor);
      insert_hydration(target, if_block_anchor, anchor);
      if (!mounted) {
        dispose = [
          listen(
            button0,
            "click",
            /*dispatch*/
            ctx[11]("up")
          ),
          listen(
            button1,
            "click",
            /*dispatch*/
            ctx[11]("left")
          ),
          listen(
            button2,
            "click",
            /*dispatch*/
            ctx[11]("right")
          ),
          listen(
            button3,
            "click",
            /*dispatch*/
            ctx[11]("down")
          )
        ];
        mounted = true;
      }
    },
    p(ctx2, dirty) {
      if (!/*is_container*/
      ctx2[1]) {
        if (if_block) {
          if_block.p(ctx2, dirty);
        } else {
          if_block = create_if_block_2(ctx2);
          if_block.c();
          if_block.m(if_block_anchor.parentNode, if_block_anchor);
        }
      } else if (if_block) {
        if_block.d(1);
        if_block = null;
      }
    },
    d(detaching) {
      if (detaching) {
        detach(button0);
        detach(t1);
        detach(button1);
        detach(t3);
        detach(button2);
        detach(t5);
        detach(button3);
        detach(t7);
        detach(if_block_anchor);
      }
      if (if_block)
        if_block.d(detaching);
      mounted = false;
      run_all(dispose);
    }
  };
}
function create_if_block(ctx) {
  let if_block_anchor;
  let if_block = !/*is_function*/
  ctx[10] && !/*is_container*/
  ctx[1] && create_if_block_1(ctx);
  return {
    c() {
      if (if_block)
        if_block.c();
      if_block_anchor = empty();
    },
    l(nodes) {
      if (if_block)
        if_block.l(nodes);
      if_block_anchor = empty();
    },
    m(target, anchor) {
      if (if_block)
        if_block.m(target, anchor);
      insert_hydration(target, if_block_anchor, anchor);
    },
    p(ctx2, dirty) {
      if (!/*is_function*/
      ctx2[10] && !/*is_container*/
      ctx2[1]) {
        if (if_block) {
          if_block.p(ctx2, dirty);
        } else {
          if_block = create_if_block_1(ctx2);
          if_block.c();
          if_block.m(if_block_anchor.parentNode, if_block_anchor);
        }
      } else if (if_block) {
        if_block.d(1);
        if_block = null;
      }
    },
    d(detaching) {
      if (detaching) {
        detach(if_block_anchor);
      }
      if (if_block)
        if_block.d(detaching);
    }
  };
}
function create_if_block_2(ctx) {
  let button0;
  let textContent = "✎";
  let t1;
  let button1;
  let textContent_1 = "✗";
  let mounted;
  let dispose;
  return {
    c() {
      button0 = element("button");
      button0.textContent = textContent;
      t1 = space();
      button1 = element("button");
      button1.textContent = textContent_1;
      this.h();
    },
    l(nodes) {
      button0 = claim_element(nodes, "BUTTON", { class: true, ["data-svelte-h"]: true });
      if (get_svelte_dataset(button0) !== "svelte-xeup1i")
        button0.textContent = textContent;
      t1 = claim_space(nodes);
      button1 = claim_element(nodes, "BUTTON", { class: true, ["data-svelte-h"]: true });
      if (get_svelte_dataset(button1) !== "svelte-ko6iaj")
        button1.textContent = textContent_1;
      this.h();
    },
    h() {
      attr(button0, "class", "action modify svelte-1ccw3kh");
      attr(button1, "class", "action delete svelte-1ccw3kh");
    },
    m(target, anchor) {
      insert_hydration(target, button0, anchor);
      insert_hydration(target, t1, anchor);
      insert_hydration(target, button1, anchor);
      if (!mounted) {
        dispose = [
          listen(
            button0,
            "click",
            /*dispatch*/
            ctx[11]("modify")
          ),
          listen(
            button1,
            "click",
            /*dispatch*/
            ctx[11]("delete")
          )
        ];
        mounted = true;
      }
    },
    p: noop,
    d(detaching) {
      if (detaching) {
        detach(button0);
        detach(t1);
        detach(button1);
      }
      mounted = false;
      run_all(dispose);
    }
  };
}
function create_if_block_1(ctx) {
  let div;
  let button0;
  let textContent = "input";
  let t1;
  let button1;
  let textContent_1 = "output";
  let t3;
  let mounted;
  let dispose;
  let each_value = ensure_array_like(
    /*event_list*/
    ctx[6]
  );
  let each_blocks = [];
  for (let i = 0; i < each_value.length; i += 1) {
    each_blocks[i] = create_each_block(get_each_context(ctx, each_value, i));
  }
  return {
    c() {
      div = element("div");
      button0 = element("button");
      button0.textContent = textContent;
      t1 = space();
      button1 = element("button");
      button1.textContent = textContent_1;
      t3 = text("\n					| ");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].c();
      }
      this.h();
    },
    l(nodes) {
      div = claim_element(nodes, "DIV", { class: true });
      var div_nodes = children(div);
      button0 = claim_element(div_nodes, "BUTTON", { class: true, ["data-svelte-h"]: true });
      if (get_svelte_dataset(button0) !== "svelte-g0b3ia")
        button0.textContent = textContent;
      t1 = claim_space(div_nodes);
      button1 = claim_element(div_nodes, "BUTTON", { class: true, ["data-svelte-h"]: true });
      if (get_svelte_dataset(button1) !== "svelte-zz2f36")
        button1.textContent = textContent_1;
      t3 = claim_text(div_nodes, "\n					| ");
      for (let i = 0; i < each_blocks.length; i += 1) {
        each_blocks[i].l(div_nodes);
      }
      div_nodes.forEach(detach);
      this.h();
    },
    h() {
      attr(button0, "class", "function input svelte-1ccw3kh");
      toggle_class(
        button0,
        "selected",
        /*is_input*/
        ctx[7]
      );
      attr(button1, "class", "function output svelte-1ccw3kh");
      toggle_class(
        button1,
        "selected",
        /*is_output*/
        ctx[8]
      );
      attr(div, "class", "button-set svelte-1ccw3kh");
    },
    m(target, anchor) {
      insert_hydration(target, div, anchor);
      append_hydration(div, button0);
      append_hydration(div, t1);
      append_hydration(div, button1);
      append_hydration(div, t3);
      for (let i = 0; i < each_blocks.length; i += 1) {
        if (each_blocks[i]) {
          each_blocks[i].m(div, null);
        }
      }
      if (!mounted) {
        dispose = [
          listen(
            button0,
            "click",
            /*dispatch*/
            ctx[11]("input")
          ),
          listen(
            button1,
            "click",
            /*dispatch*/
            ctx[11]("output")
          )
        ];
        mounted = true;
      }
    },
    p(ctx2, dirty) {
      if (dirty & /*is_input*/
      128) {
        toggle_class(
          button0,
          "selected",
          /*is_input*/
          ctx2[7]
        );
      }
      if (dirty & /*is_output*/
      256) {
        toggle_class(
          button1,
          "selected",
          /*is_output*/
          ctx2[8]
        );
      }
      if (dirty & /*triggers, event_list, dispatch*/
      2624) {
        each_value = ensure_array_like(
          /*event_list*/
          ctx2[6]
        );
        let i;
        for (i = 0; i < each_value.length; i += 1) {
          const child_ctx = get_each_context(ctx2, each_value, i);
          if (each_blocks[i]) {
            each_blocks[i].p(child_ctx, dirty);
          } else {
            each_blocks[i] = create_each_block(child_ctx);
            each_blocks[i].c();
            each_blocks[i].m(div, null);
          }
        }
        for (; i < each_blocks.length; i += 1) {
          each_blocks[i].d(1);
        }
        each_blocks.length = each_value.length;
      }
    },
    d(detaching) {
      if (detaching) {
        detach(div);
      }
      destroy_each(each_blocks, detaching);
      mounted = false;
      run_all(dispose);
    }
  };
}
function create_each_block(ctx) {
  let button;
  let t0;
  let t1_value = (
    /*event*/
    ctx[16] + ""
  );
  let t1;
  let mounted;
  let dispose;
  return {
    c() {
      button = element("button");
      t0 = text("on:");
      t1 = text(t1_value);
      this.h();
    },
    l(nodes) {
      button = claim_element(nodes, "BUTTON", { class: true });
      var button_nodes = children(button);
      t0 = claim_text(button_nodes, "on:");
      t1 = claim_text(button_nodes, t1_value);
      button_nodes.forEach(detach);
      this.h();
    },
    h() {
      attr(button, "class", "function event svelte-1ccw3kh");
      toggle_class(
        button,
        "selected",
        /*triggers*/
        ctx[9].includes(
          /*event*/
          ctx[16]
        )
      );
    },
    m(target, anchor) {
      insert_hydration(target, button, anchor);
      append_hydration(button, t0);
      append_hydration(button, t1);
      if (!mounted) {
        dispose = listen(button, "click", function() {
          if (is_function(
            /*dispatch*/
            ctx[11]("on:" + /*event*/
            ctx[16])
          ))
            ctx[11]("on:" + /*event*/
            ctx[16]).apply(this, arguments);
        });
        mounted = true;
      }
    },
    p(new_ctx, dirty) {
      ctx = new_ctx;
      if (dirty & /*event_list*/
      64 && t1_value !== (t1_value = /*event*/
      ctx[16] + ""))
        set_data(t1, t1_value);
      if (dirty & /*triggers, event_list*/
      576) {
        toggle_class(
          button,
          "selected",
          /*triggers*/
          ctx[9].includes(
            /*event*/
            ctx[16]
          )
        );
      }
    },
    d(detaching) {
      if (detaching) {
        detach(button);
      }
      mounted = false;
      dispose();
    }
  };
}
function create_fragment(ctx) {
  let div2;
  let div0;
  let t0;
  let div1;
  let show_if = (
    /*invisible_components*/
    ctx[12].includes(
      /*component_type*/
      ctx[2]
    )
  );
  let t1;
  let t2;
  let current;
  let mounted;
  let dispose;
  let if_block0 = show_if && create_if_block_3(ctx);
  function select_block_type(ctx2, dirty) {
    if (
      /*function_mode*/
      ctx2[5]
    )
      return create_if_block;
    return create_else_block;
  }
  let current_block_type = select_block_type(ctx);
  let if_block1 = current_block_type(ctx);
  const default_slot_template = (
    /*#slots*/
    ctx[15].default
  );
  const default_slot = create_slot(
    default_slot_template,
    ctx,
    /*$$scope*/
    ctx[14],
    null
  );
  return {
    c() {
      div2 = element("div");
      div0 = element("div");
      t0 = space();
      div1 = element("div");
      if (if_block0)
        if_block0.c();
      t1 = space();
      if_block1.c();
      t2 = space();
      if (default_slot)
        default_slot.c();
      this.h();
    },
    l(nodes) {
      div2 = claim_element(nodes, "DIV", { class: true });
      var div2_nodes = children(div2);
      div0 = claim_element(div2_nodes, "DIV", { class: true });
      children(div0).forEach(detach);
      t0 = claim_space(div2_nodes);
      div1 = claim_element(div2_nodes, "DIV", { class: true });
      var div1_nodes = children(div1);
      if (if_block0)
        if_block0.l(div1_nodes);
      t1 = claim_space(div1_nodes);
      if_block1.l(div1_nodes);
      div1_nodes.forEach(detach);
      t2 = claim_space(div2_nodes);
      if (default_slot)
        default_slot.l(div2_nodes);
      div2_nodes.forEach(detach);
      this.h();
    },
    h() {
      attr(div0, "class", "cover svelte-1ccw3kh");
      attr(div1, "class", "interaction svelte-1ccw3kh");
      attr(div2, "class", "sketchbox svelte-1ccw3kh");
      toggle_class(
        div2,
        "function_mode",
        /*function_mode*/
        ctx[5]
      );
      toggle_class(
        div2,
        "row",
        /*row*/
        ctx[0]
      );
      toggle_class(
        div2,
        "active",
        /*active*/
        ctx[4]
      );
    },
    m(target, anchor) {
      insert_hydration(target, div2, anchor);
      append_hydration(div2, div0);
      append_hydration(div2, t0);
      append_hydration(div2, div1);
      if (if_block0)
        if_block0.m(div1, null);
      append_hydration(div1, t1);
      if_block1.m(div1, null);
      append_hydration(div2, t2);
      if (default_slot) {
        default_slot.m(div2, null);
      }
      current = true;
      if (!mounted) {
        dispose = listen(div1, "click", function() {
          if (is_function(
            /*is_container*/
            ctx[1] ? void 0 : (
              /*dispatch*/
              ctx[11]("modify")
            )
          ))
            /*is_container*/
            (ctx[1] ? void 0 : (
              /*dispatch*/
              ctx[11]("modify")
            )).apply(this, arguments);
        });
        mounted = true;
      }
    },
    p(new_ctx, [dirty]) {
      ctx = new_ctx;
      if (dirty & /*component_type*/
      4)
        show_if = /*invisible_components*/
        ctx[12].includes(
          /*component_type*/
          ctx[2]
        );
      if (show_if) {
        if (if_block0) {
          if_block0.p(ctx, dirty);
        } else {
          if_block0 = create_if_block_3(ctx);
          if_block0.c();
          if_block0.m(div1, t1);
        }
      } else if (if_block0) {
        if_block0.d(1);
        if_block0 = null;
      }
      if (current_block_type === (current_block_type = select_block_type(ctx)) && if_block1) {
        if_block1.p(ctx, dirty);
      } else {
        if_block1.d(1);
        if_block1 = current_block_type(ctx);
        if (if_block1) {
          if_block1.c();
          if_block1.m(div1, null);
        }
      }
      if (default_slot) {
        if (default_slot.p && (!current || dirty & /*$$scope*/
        16384)) {
          update_slot_base(
            default_slot,
            default_slot_template,
            ctx,
            /*$$scope*/
            ctx[14],
            !current ? get_all_dirty_from_scope(
              /*$$scope*/
              ctx[14]
            ) : get_slot_changes(
              default_slot_template,
              /*$$scope*/
              ctx[14],
              dirty,
              null
            ),
            null
          );
        }
      }
      if (!current || dirty & /*function_mode*/
      32) {
        toggle_class(
          div2,
          "function_mode",
          /*function_mode*/
          ctx[5]
        );
      }
      if (!current || dirty & /*row*/
      1) {
        toggle_class(
          div2,
          "row",
          /*row*/
          ctx[0]
        );
      }
      if (!current || dirty & /*active*/
      16) {
        toggle_class(
          div2,
          "active",
          /*active*/
          ctx[4]
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
      if (if_block0)
        if_block0.d();
      if_block1.d();
      if (default_slot)
        default_slot.d(detaching);
      mounted = false;
      dispose();
    }
  };
}
function instance($$self, $$props, $$invalidate) {
  let is_function2;
  let { $$slots: slots = {}, $$scope } = $$props;
  let { row } = $$props;
  let { is_container } = $$props;
  let { component_type } = $$props;
  let { var_name } = $$props;
  let { active = false } = $$props;
  let { function_mode = false } = $$props;
  let { event_list } = $$props;
  let { is_input = false } = $$props;
  let { is_output = false } = $$props;
  let { triggers = [] } = $$props;
  let { gradio } = $$props;
  const dispatch = (type) => {
    return (event) => {
      event.stopPropagation();
      gradio.dispatch("select", { index: 0, value: type });
    };
  };
  const invisible_components = ["state", "browserstate", "function"];
  $$self.$$set = ($$props2) => {
    if ("row" in $$props2)
      $$invalidate(0, row = $$props2.row);
    if ("is_container" in $$props2)
      $$invalidate(1, is_container = $$props2.is_container);
    if ("component_type" in $$props2)
      $$invalidate(2, component_type = $$props2.component_type);
    if ("var_name" in $$props2)
      $$invalidate(3, var_name = $$props2.var_name);
    if ("active" in $$props2)
      $$invalidate(4, active = $$props2.active);
    if ("function_mode" in $$props2)
      $$invalidate(5, function_mode = $$props2.function_mode);
    if ("event_list" in $$props2)
      $$invalidate(6, event_list = $$props2.event_list);
    if ("is_input" in $$props2)
      $$invalidate(7, is_input = $$props2.is_input);
    if ("is_output" in $$props2)
      $$invalidate(8, is_output = $$props2.is_output);
    if ("triggers" in $$props2)
      $$invalidate(9, triggers = $$props2.triggers);
    if ("gradio" in $$props2)
      $$invalidate(13, gradio = $$props2.gradio);
    if ("$$scope" in $$props2)
      $$invalidate(14, $$scope = $$props2.$$scope);
  };
  $$self.$$.update = () => {
    if ($$self.$$.dirty & /*component_type*/
    4) {
      $$invalidate(10, is_function2 = component_type === "function");
    }
  };
  return [
    row,
    is_container,
    component_type,
    var_name,
    active,
    function_mode,
    event_list,
    is_input,
    is_output,
    triggers,
    is_function2,
    dispatch,
    invisible_components,
    gradio,
    $$scope,
    slots
  ];
}
class Index extends SvelteComponent {
  constructor(options) {
    super();
    init(this, options, instance, create_fragment, safe_not_equal, {
      row: 0,
      is_container: 1,
      component_type: 2,
      var_name: 3,
      active: 4,
      function_mode: 5,
      event_list: 6,
      is_input: 7,
      is_output: 8,
      triggers: 9,
      gradio: 13
    });
  }
}
export {
  Index as default
};
