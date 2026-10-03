import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the jupyterlab_mechanicum_dark_theme extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_mechanicum_dark_theme:plugin',
  description:
    'Dark Adeptus Mechanicum theme: crimson cloth, gold embroidery, steel and parchment',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log(
      'JupyterLab extension jupyterlab_mechanicum_dark_theme is activated!'
    );
    const style = 'jupyterlab_mechanicum_dark_theme/index.css';

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
