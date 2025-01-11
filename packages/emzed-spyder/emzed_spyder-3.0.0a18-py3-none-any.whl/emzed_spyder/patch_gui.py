#! /usr/bin/env python
# Copyright 2020 Uwe Schmitt <uwe.schmitt@id.ethz.ch>

from importlib.metadata import version

from .utils import get_active_project, get_project_folder


def patch_double_click_variable_explorer():
    from spyder.plugins.variableexplorer.widgets.collectionsdelegate import (
        CollectionsDelegate,
    )

    def createEditor(
        self,
        parent,
        option,
        index,
        object_explorer=False,
        _orig=CollectionsDelegate.createEditor,
    ):
        """
        this method is triggered by double click in the variable explorer table widget.
        """
        if index.column() < 3:
            return None

        # This is a tricky patch: default is that spyder loads the data from the remote
        # shell process into the spyder process. We patch this method such that emzed
        # tables and peakmaps are shown from the remote shell process to avoid data
        # copying and to
        # support persistent editing.

        # type_ = model.row_type(row_num)
        model = index.model()

        if hasattr(model, "sourceModel"):
            ns_view_table_model = model.sourceModel()
            internal_index = model.mapToSource(index)
            type_ = ns_view_table_model.types[internal_index.row()]

            # no isinstance checks here as we have no access to the real object in the
            # remote shell:
            if type_ in ("Table", "PeakMap", "ImmutablePeakMap"):
                variable_name = ns_view_table_model.get_key(internal_index)
                print("inspect", repr(variable_name))
                sw = ns_view_table_model._parent.shellwidget
                sw.execute(
                    f"_inspect({variable_name}, modal=False);",
                    hidden=True,
                )
                return None

        return _orig(self, parent, option, index, object_explorer)

    CollectionsDelegate.createEditor = createEditor


def patch_window_title():
    from spyder.app.mainwindow import MainWindow

    emzed_spyder_version = version(__package__)

    def set_window_title(self, _orig=MainWindow.set_window_title):
        _orig(self)
        fixed_title = self.base_title.replace(
            "Spyder", f"emzed.spyder {emzed_spyder_version}"
        )
        self.base_title = fixed_title
        self.setWindowTitle(fixed_title)

    MainWindow.set_window_title = set_window_title


def activate_file_browser():
    from spyder.app.mainwindow import MainWindow

    def post_visible_setup(self, _orig=MainWindow.post_visible_setup):
        _orig(self)
        self.explorer.dockwidget.raise_()

    MainWindow.post_visible_setup = post_visible_setup


def patch_editor_code_completion():
    from spyder.plugins.editor.widgets.completion import (
        CompletionItemKind,
        CompletionWidget,
    )

    ok = (
        CompletionItemKind.METHOD,
        CompletionItemKind.FUNCTION,
        CompletionItemKind.FIELD,
        CompletionItemKind.VARIABLE,
        CompletionItemKind.CLASS,
        CompletionItemKind.KEYWORD,
    )

    def show_list(
        self, completion_list, position, automatic, _orig=CompletionWidget.show_list
    ):
        def should_be_shown(item):
            label = item["label"]
            kind = item["kind"]
            return kind in ok and not label.startswith("_")

            # detail might not be set  in the fallback mode (happens e.g. when pyls
            # times out):
            detail = item.get("detail", "emzed")
            if detail.startswith("emzed") and label.startswith("_"):
                return False
            if kind in (CompletionItemKind.TEXT,):
                return False
            if kind == CompletionItemKind.CLASS and (
                label.endswith("Error") or label.endswith("Warning")
            ):
                return False
            return True

        completion_list = [item for item in completion_list if should_be_shown(item)]
        completion_list.sort(key=lambda item: item["label"].upper())
        return _orig(self, completion_list, position, automatic)

    CompletionWidget.show_list = show_list


def patch_in_prompt():
    import qtconsole.jupyter_widget as jw

    from .utils import get_active_project, is_valid_project

    # prompt unique per session
    cache = {}

    def get_prompt(obj):
        key = id(obj)
        if key not in cache:
            active_project = get_active_project()
            if active_project is not None and is_valid_project(active_project):
                prompt = f"({active_project}) " + jw.default_in_prompt
            else:
                prompt = jw.default_in_prompt
            cache[key] = prompt
        return cache[key]

    class DynamicInPrompt:
        def __get__(self, obj, type_=None):
            return get_prompt(obj)

    jw.JupyterWidget.in_prompt = DynamicInPrompt()


def patch_console_startup():
    from spyder.plugins.ipythonconsole.widgets.client import ClientWidget

    def _set_initial_cwd_in_kernel(self, _orig=ClientWidget._set_initial_cwd_in_kernel):
        active_project = get_active_project()
        if not active_project:
            _orig(self)
            return
        folder = get_project_folder(active_project)
        try:
            if folder.is_dir():
                self.shellwidget.set_cwd(str(folder), emit_cwd_change=True)
        except Exception as e:
            print(e)
            _orig(self)

    ClientWidget._set_initial_cwd_in_kernel = _set_initial_cwd_in_kernel
