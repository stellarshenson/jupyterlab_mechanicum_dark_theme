import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the @stellarshenson/jupyterlab-mechanicum-dark-theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: '@stellarshenson/jupyterlab-mechanicum-dark-theme:plugin',
  description:
    'Dark Adeptus Mechanicum theme: crimson cloth, gold embroidery, steel and parchment',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log(
      'JupyterLab extension @stellarshenson/jupyterlab-mechanicum-dark-theme is activated!'
    );
    const style = '@stellarshenson/jupyterlab-mechanicum-dark-theme/index.css';

    manager.register({
      name: 'Mechanicum Dark Theme',
      themeScrollbars: true,
      isLight: false,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
