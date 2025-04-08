import { c as create_ssr_component, v as validate_component, a as createEventDispatcher, e as escape, b as add_attribute } from './ssr-FJHii0oS.js';
import { S as Static, I as Index$1 } from './2-DeykbhT8.js';
import './index-BJuG1GWC.js';
import 'tty';
import 'path';
import 'url';
import 'fs';
import './Component--bfMfOuT.js';

const css = {
  code: "@media(max-width: 768px){.sidebar.svelte-y4v1h1.svelte-y4v1h1{width:100vw !important}.sidebar.svelte-y4v1h1.svelte-y4v1h1:not(.right){left:-100vw !important}.sidebar.right.svelte-y4v1h1.svelte-y4v1h1{right:-100vw !important}.sidebar.svelte-y4v1h1.svelte-y4v1h1:not(.reduce-motion){transition:transform 0.3s ease-in-out !important}.sidebar-parent{padding-left:0 !important;padding-right:0 !important}.sidebar-parent:has(.sidebar.open){padding-left:0 !important;padding-right:0 !important}.sidebar.open.svelte-y4v1h1.svelte-y4v1h1{z-index:1001 !important}}.sidebar-parent{display:flex !important;padding-left:0;padding-right:0}.sidebar-parent:not(.reduce-motion){transition:padding-left 0.3s ease-in-out,\n			padding-right 0.3s ease-in-out}.sidebar-parent:has(.sidebar.open:not(.right)){padding-left:var(--overlap-amount)}.sidebar-parent:has(.sidebar.open.right){padding-right:var(--overlap-amount)}.sidebar.svelte-y4v1h1.svelte-y4v1h1{display:flex;flex-direction:column;position:fixed;top:0;height:100%;background-color:var(--background-fill-secondary);transform:translateX(0%);z-index:1000}.sidebar.svelte-y4v1h1.svelte-y4v1h1:not(.reduce-motion){transition:transform 0.3s ease-in-out}.sidebar.open.svelte-y4v1h1.svelte-y4v1h1:not(.right){transform:translateX(100%);box-shadow:var(--size-1) 0 var(--size-2) rgba(100, 89, 89, 0.1)}.sidebar.open.right.svelte-y4v1h1.svelte-y4v1h1{transform:translateX(-100%);box-shadow:calc(var(--size-1) * -1) 0 var(--size-2) rgba(100, 89, 89, 0.1)}.toggle-button.svelte-y4v1h1.svelte-y4v1h1{position:absolute;top:var(--size-4);background:none;border:none;cursor:pointer;padding:var(--size-2);display:flex;align-items:center;justify-content:center;width:var(--size-8);height:var(--size-8);z-index:1001}.toggle-button.svelte-y4v1h1.svelte-y4v1h1:not(.reduce-motion){transition:all 0.3s ease-in-out}.sidebar.svelte-y4v1h1:not(.right) .toggle-button.svelte-y4v1h1{right:calc(var(--size-8) * -1)}.sidebar.right.svelte-y4v1h1 .toggle-button.svelte-y4v1h1{left:calc(var(--size-8) * -1);transform:rotate(180deg)}.open.svelte-y4v1h1:not(.right) .toggle-button.svelte-y4v1h1{right:var(--size-2-5);transform:rotate(180deg)}.open.right.svelte-y4v1h1 .toggle-button.svelte-y4v1h1{left:auto;right:var(--size-2-5);transform:rotate(0deg)}.chevron.svelte-y4v1h1.svelte-y4v1h1{width:100%;height:100%;position:relative;display:flex;align-items:center;justify-content:center}.chevron-left.svelte-y4v1h1.svelte-y4v1h1{position:relative;width:var(--size-3);height:var(--size-3);border-top:var(--size-0-5) solid var(--button-secondary-text-color);border-right:var(--size-0-5) solid var(--button-secondary-text-color);transform:rotate(45deg)}.sidebar-content.svelte-y4v1h1.svelte-y4v1h1{padding:var(--size-5);padding-right:var(--size-8);overflow-y:auto}.sidebar.right.svelte-y4v1h1 .sidebar-content.svelte-y4v1h1{padding-left:var(--size-8)}",
  map: '{"version":3,"file":"Sidebar.svelte","sources":["Sidebar.svelte"],"sourcesContent":["<script lang=\\"ts\\">import { createEventDispatcher, onMount } from \\"svelte\\";\\nconst dispatch = createEventDispatcher();\\nexport let open = true;\\nexport let width;\\nexport let position = \\"left\\";\\nlet mounted = false;\\nlet _open = false;\\nlet sidebar_div;\\nlet overlap_amount = 0;\\nlet width_css = typeof width === \\"number\\" ? `${width}px` : width;\\nlet prefersReducedMotion;\\nfunction check_overlap() {\\n    if (!sidebar_div.closest(\\".wrap\\"))\\n        return;\\n    const parent_rect = sidebar_div.closest(\\".wrap\\")?.getBoundingClientRect();\\n    if (!parent_rect)\\n        return;\\n    const sidebar_rect = sidebar_div.getBoundingClientRect();\\n    const available_space = position === \\"left\\" ? parent_rect.left : window.innerWidth - parent_rect.right;\\n    overlap_amount = Math.max(0, sidebar_rect.width - available_space + 30);\\n}\\nonMount(() => {\\n    sidebar_div.closest(\\".wrap\\")?.classList.add(\\"sidebar-parent\\");\\n    check_overlap();\\n    window.addEventListener(\\"resize\\", check_overlap);\\n    const update_parent_overlap = () => {\\n        document.documentElement.style.setProperty(\\"--overlap-amount\\", `${overlap_amount}px`);\\n    };\\n    update_parent_overlap();\\n    mounted = true;\\n    const mediaQuery = window.matchMedia(\\"(prefers-reduced-motion: reduce)\\");\\n    prefersReducedMotion = mediaQuery.matches;\\n    const updateMotionPreference = (e) => {\\n        prefersReducedMotion = e.matches;\\n    };\\n    mediaQuery.addEventListener(\\"change\\", updateMotionPreference);\\n    return () => {\\n        window.removeEventListener(\\"resize\\", check_overlap);\\n        mediaQuery.removeEventListener(\\"change\\", updateMotionPreference);\\n    };\\n});\\n$: if (mounted)\\n    _open = open;\\n<\/script>\\n\\n<div\\n\\tclass=\\"sidebar\\"\\n\\tclass:open={_open}\\n\\tclass:right={position === \\"right\\"}\\n\\tclass:reduce-motion={prefersReducedMotion}\\n\\tbind:this={sidebar_div}\\n\\tstyle=\\"width: {width_css}; {position}: calc({width_css} * -1)\\"\\n>\\n\\t<button\\n\\t\\ton:click={() => {\\n\\t\\t\\t_open = !_open;\\n\\t\\t\\tif (_open) {\\n\\t\\t\\t\\tdispatch(\\"expand\\");\\n\\t\\t\\t} else {\\n\\t\\t\\t\\tdispatch(\\"collapse\\");\\n\\t\\t\\t}\\n\\t\\t}}\\n\\t\\tclass=\\"toggle-button\\"\\n\\t\\taria-label=\\"Toggle Sidebar\\"\\n\\t>\\n\\t\\t<div class=\\"chevron\\">\\n\\t\\t\\t<span class=\\"chevron-left\\"></span>\\n\\t\\t</div>\\n\\t</button>\\n\\t<div class=\\"sidebar-content\\">\\n\\t\\t<slot />\\n\\t</div>\\n</div>\\n\\n<style>\\n\\t/* Mobile styles (≤ 768px) */\\n\\t@media (max-width: 768px) {\\n\\t\\t.sidebar {\\n\\t\\t\\twidth: 100vw !important;\\n\\t\\t}\\n\\n\\t\\t.sidebar:not(.right) {\\n\\t\\t\\tleft: -100vw !important;\\n\\t\\t}\\n\\n\\t\\t.sidebar.right {\\n\\t\\t\\tright: -100vw !important;\\n\\t\\t}\\n\\n\\t\\t.sidebar:not(.reduce-motion) {\\n\\t\\t\\ttransition: transform 0.3s ease-in-out !important;\\n\\t\\t}\\n\\n\\t\\t:global(.sidebar-parent) {\\n\\t\\t\\tpadding-left: 0 !important;\\n\\t\\t\\tpadding-right: 0 !important;\\n\\t\\t}\\n\\n\\t\\t:global(.sidebar-parent:has(.sidebar.open)) {\\n\\t\\t\\tpadding-left: 0 !important;\\n\\t\\t\\tpadding-right: 0 !important;\\n\\t\\t}\\n\\t\\t.sidebar.open {\\n\\t\\t\\tz-index: 1001 !important;\\n\\t\\t}\\n\\t}\\n\\n\\t:global(.sidebar-parent) {\\n\\t\\tdisplay: flex !important;\\n\\t\\tpadding-left: 0;\\n\\t\\tpadding-right: 0;\\n\\t}\\n\\n\\t:global(.sidebar-parent:not(.reduce-motion)) {\\n\\t\\ttransition:\\n\\t\\t\\tpadding-left 0.3s ease-in-out,\\n\\t\\t\\tpadding-right 0.3s ease-in-out;\\n\\t}\\n\\n\\t:global(.sidebar-parent:has(.sidebar.open:not(.right))) {\\n\\t\\tpadding-left: var(--overlap-amount);\\n\\t}\\n\\n\\t:global(.sidebar-parent:has(.sidebar.open.right)) {\\n\\t\\tpadding-right: var(--overlap-amount);\\n\\t}\\n\\n\\t.sidebar {\\n\\t\\tdisplay: flex;\\n\\t\\tflex-direction: column;\\n\\t\\tposition: fixed;\\n\\t\\ttop: 0;\\n\\t\\theight: 100%;\\n\\t\\tbackground-color: var(--background-fill-secondary);\\n\\t\\ttransform: translateX(0%);\\n\\t\\tz-index: 1000;\\n\\t}\\n\\n\\t.sidebar:not(.reduce-motion) {\\n\\t\\ttransition: transform 0.3s ease-in-out;\\n\\t}\\n\\n\\t.sidebar.open:not(.right) {\\n\\t\\ttransform: translateX(100%);\\n\\t\\tbox-shadow: var(--size-1) 0 var(--size-2) rgba(100, 89, 89, 0.1);\\n\\t}\\n\\n\\t.sidebar.open.right {\\n\\t\\ttransform: translateX(-100%);\\n\\t\\tbox-shadow: calc(var(--size-1) * -1) 0 var(--size-2) rgba(100, 89, 89, 0.1);\\n\\t}\\n\\n\\t.toggle-button {\\n\\t\\tposition: absolute;\\n\\t\\ttop: var(--size-4);\\n\\t\\tbackground: none;\\n\\t\\tborder: none;\\n\\t\\tcursor: pointer;\\n\\t\\tpadding: var(--size-2);\\n\\t\\tdisplay: flex;\\n\\t\\talign-items: center;\\n\\t\\tjustify-content: center;\\n\\t\\twidth: var(--size-8);\\n\\t\\theight: var(--size-8);\\n\\t\\tz-index: 1001;\\n\\t}\\n\\n\\t.toggle-button:not(.reduce-motion) {\\n\\t\\ttransition: all 0.3s ease-in-out;\\n\\t}\\n\\n\\t.sidebar:not(.right) .toggle-button {\\n\\t\\tright: calc(var(--size-8) * -1);\\n\\t}\\n\\n\\t.sidebar.right .toggle-button {\\n\\t\\tleft: calc(var(--size-8) * -1);\\n\\t\\ttransform: rotate(180deg);\\n\\t}\\n\\n\\t.open:not(.right) .toggle-button {\\n\\t\\tright: var(--size-2-5);\\n\\t\\ttransform: rotate(180deg);\\n\\t}\\n\\n\\t.open.right .toggle-button {\\n\\t\\tleft: auto;\\n\\t\\tright: var(--size-2-5);\\n\\t\\ttransform: rotate(0deg);\\n\\t}\\n\\n\\t.chevron {\\n\\t\\twidth: 100%;\\n\\t\\theight: 100%;\\n\\t\\tposition: relative;\\n\\t\\tdisplay: flex;\\n\\t\\talign-items: center;\\n\\t\\tjustify-content: center;\\n\\t}\\n\\n\\t.chevron-left {\\n\\t\\tposition: relative;\\n\\t\\twidth: var(--size-3);\\n\\t\\theight: var(--size-3);\\n\\t\\tborder-top: var(--size-0-5) solid var(--button-secondary-text-color);\\n\\t\\tborder-right: var(--size-0-5) solid var(--button-secondary-text-color);\\n\\t\\ttransform: rotate(45deg);\\n\\t}\\n\\n\\t.sidebar-content {\\n\\t\\tpadding: var(--size-5);\\n\\t\\tpadding-right: var(--size-8);\\n\\t\\toverflow-y: auto;\\n\\t}\\n\\n\\t.sidebar.right .sidebar-content {\\n\\t\\tpadding-left: var(--size-8);\\n\\t}</style>\\n"],"names":[],"mappings":"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"}'
};
const Sidebar = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  createEventDispatcher();
  let { open = true } = $$props;
  let { width } = $$props;
  let { position = "left" } = $$props;
  let sidebar_div;
  let width_css = typeof width === "number" ? `${width}px` : width;
  if ($$props.open === void 0 && $$bindings.open && open !== void 0)
    $$bindings.open(open);
  if ($$props.width === void 0 && $$bindings.width && width !== void 0)
    $$bindings.width(width);
  if ($$props.position === void 0 && $$bindings.position && position !== void 0)
    $$bindings.position(position);
  $$result.css.add(css);
  return `<div class="${[
    "sidebar svelte-y4v1h1",
    ("") + " " + (position === "right" ? "right" : "") + " " + ("")
  ].join(" ").trim()}" style="${"width: " + escape(width_css, true) + "; " + escape(position, true) + ": calc(" + escape(width_css, true) + " * -1)"}"${add_attribute("this", sidebar_div, 0)}><button class="toggle-button svelte-y4v1h1" aria-label="Toggle Sidebar" data-svelte-h="svelte-k78zcg"><div class="chevron svelte-y4v1h1"><span class="chevron-left svelte-y4v1h1"></span></div></button> <div class="sidebar-content svelte-y4v1h1">${slots.default ? slots.default({}) : ``}</div> </div>`;
});
const Index = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { open = true } = $$props;
  let { position = "left" } = $$props;
  let { loading_status } = $$props;
  let { gradio } = $$props;
  let { width } = $$props;
  let { visible = true } = $$props;
  if ($$props.open === void 0 && $$bindings.open && open !== void 0)
    $$bindings.open(open);
  if ($$props.position === void 0 && $$bindings.position && position !== void 0)
    $$bindings.position(position);
  if ($$props.loading_status === void 0 && $$bindings.loading_status && loading_status !== void 0)
    $$bindings.loading_status(loading_status);
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  if ($$props.width === void 0 && $$bindings.width && width !== void 0)
    $$bindings.width(width);
  if ($$props.visible === void 0 && $$bindings.visible && visible !== void 0)
    $$bindings.visible(visible);
  let $$settled;
  let $$rendered;
  let previous_head = $$result.head;
  do {
    $$settled = true;
    $$result.head = previous_head;
    $$rendered = `${validate_component(Static, "StatusTracker").$$render($$result, Object.assign({}, { autoscroll: gradio.autoscroll }, { i18n: gradio.i18n }, loading_status), {}, {})} ${visible ? `${validate_component(Sidebar, "Sidebar").$$render(
      $$result,
      { width, open, position },
      {
        open: ($$value) => {
          open = $$value;
          $$settled = false;
        },
        position: ($$value) => {
          position = $$value;
          $$settled = false;
        }
      },
      {
        default: () => {
          return `${validate_component(Index$1, "Column").$$render($$result, {}, {}, {
            default: () => {
              return `${slots.default ? slots.default({}) : ``}`;
            }
          })}`;
        }
      }
    )}` : ``}`;
  } while (!$$settled);
  return $$rendered;
});

export { Index as default };
//# sourceMappingURL=Index41--ESjJOaE.js.map
