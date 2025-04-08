import { c as create_ssr_component, a as createEventDispatcher, v as validate_component, m as missing_component } from './ssr-FJHii0oS.js';
import { h as Empty, aE as Plot$1 } from './2-DeykbhT8.js';
import './index-BJuG1GWC.js';
import 'tty';
import 'path';
import 'url';
import 'fs';
import './Component--bfMfOuT.js';

const Plot = create_ssr_component(($$result, $$props, $$bindings, slots) => {
  let { value } = $$props;
  let _value;
  let { colors = [] } = $$props;
  let { show_label } = $$props;
  let { theme_mode } = $$props;
  let { caption } = $$props;
  let { bokeh_version } = $$props;
  let { show_actions_button } = $$props;
  let { gradio } = $$props;
  let { x_lim = null } = $$props;
  let { _selectable } = $$props;
  let PlotComponent = null;
  let _type = value?.type;
  let loaded_plotly_css = false;
  const dispatch = createEventDispatcher();
  const plotTypeMapping = {
    plotly: () => import('./PlotlyPlot-Dj_i3J5T.js'),
    bokeh: () => import('./BokehPlot-BocoOPbP.js'),
    altair: () => import('./AltairPlot-BqjrpFOv.js'),
    matplotlib: () => import('./MatplotlibPlot-ZMZOYfvS.js')
  };
  let loadedPlotTypeMapping = {};
  const is_browser = typeof window !== "undefined";
  if ($$props.value === void 0 && $$bindings.value && value !== void 0)
    $$bindings.value(value);
  if ($$props.colors === void 0 && $$bindings.colors && colors !== void 0)
    $$bindings.colors(colors);
  if ($$props.show_label === void 0 && $$bindings.show_label && show_label !== void 0)
    $$bindings.show_label(show_label);
  if ($$props.theme_mode === void 0 && $$bindings.theme_mode && theme_mode !== void 0)
    $$bindings.theme_mode(theme_mode);
  if ($$props.caption === void 0 && $$bindings.caption && caption !== void 0)
    $$bindings.caption(caption);
  if ($$props.bokeh_version === void 0 && $$bindings.bokeh_version && bokeh_version !== void 0)
    $$bindings.bokeh_version(bokeh_version);
  if ($$props.show_actions_button === void 0 && $$bindings.show_actions_button && show_actions_button !== void 0)
    $$bindings.show_actions_button(show_actions_button);
  if ($$props.gradio === void 0 && $$bindings.gradio && gradio !== void 0)
    $$bindings.gradio(gradio);
  if ($$props.x_lim === void 0 && $$bindings.x_lim && x_lim !== void 0)
    $$bindings.x_lim(x_lim);
  if ($$props._selectable === void 0 && $$bindings._selectable && _selectable !== void 0)
    $$bindings._selectable(_selectable);
  let $$settled;
  let $$rendered;
  let previous_head = $$result.head;
  do {
    $$settled = true;
    $$result.head = previous_head;
    {
      if (value !== _value) {
        let type = value?.type;
        if (type !== _type) {
          PlotComponent = null;
        }
        if (type && type in plotTypeMapping && is_browser) {
          if (loadedPlotTypeMapping[type]) {
            PlotComponent = loadedPlotTypeMapping[type];
          } else {
            plotTypeMapping[type]().then((module) => {
              PlotComponent = module.default;
              loadedPlotTypeMapping[type] = PlotComponent;
            });
          }
        }
        _value = value;
        _type = type;
        dispatch("change");
      }
    }
    $$rendered = `${value && PlotComponent ? `${validate_component(PlotComponent || missing_component, "svelte:component").$$render(
      $$result,
      {
        value,
        colors,
        theme_mode,
        show_label,
        caption,
        bokeh_version,
        show_actions_button,
        gradio,
        _selectable,
        x_lim,
        loaded_plotly_css
      },
      {
        loaded_plotly_css: ($$value) => {
          loaded_plotly_css = $$value;
          $$settled = false;
        }
      },
      {}
    )}` : `${validate_component(Empty, "Empty").$$render($$result, { unpadded_box: true, size: "large" }, {}, {
      default: () => {
        return `${validate_component(Plot$1, "PlotIcon").$$render($$result, {}, {}, {})}`;
      }
    })}`}`;
  } while (!$$settled);
  return $$rendered;
});

export { Plot as default };
//# sourceMappingURL=Plot-CuwWRFJI.js.map
