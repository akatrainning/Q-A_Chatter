import { c as create_ssr_component, e as escape } from './ssr-FJHii0oS.js';

const Example = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value } = $$props;
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  return `${escape(value || "")}`;
});

export { Example as default };
//# sourceMappingURL=Example-39PswHWL.js.map
