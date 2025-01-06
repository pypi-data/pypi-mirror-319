"""
user preferences widgets for your kivy app
==========================================

This namespace portion is providing a set of widgets to allow the users of your app to change their personal
app states/settings/preferences, like the theme, the font size, the language and the used colors.

To use it in your app import this module, which can be done either in one of the modules of your app via::

    import ae.kivy_user_prefs

Alternatively and when you use the `Kivy framework <https://kivy.org>`__ for your app, you can import it
within your main KV file, like this::

    #: import _any_dummy_name ae.kivy_user_prefs

.. note::
    The i18n translation texts of this namespace portion are provided mainly by the portion :mod:`ae.i18n`, registered
    on import of it, and the color names by :mod:`ae.gui_help`. So when you import this portion from the main KV file
    of your app, and your app is overwriting a translation text of this portion, then you have to make sure
    that the translation texts of your main app get registered after the import of this portion. For that reason
    :class:`~ae.gui_app.MainAppBase` is using the `on_app_build` event to load the application resources,
    which gets fired after Kivy has imported the main KV file.


The user preferences are implemented as a :class:`~ae.kivy.widgets.FlowDropDown` via the widget `UserPreferencesPopup`.

To integrate it in your app you simply add the `UserPreferencesButton` widget to the main KV file of your app.


user preferences debug mode
---------------------------

The user preferences are activating a debug mode when you click/touch the `UserPreferencesButton` button more than three
times within 6 seconds.

This debug mode activation is implemented in the :meth:`~ae.kivy.apps.KivyMainApp.on_user_preferences_open`  event
handler method declared in the :mod:`ae.kivy.apps` module. It can be disabled for your app by simply overriding this
method with an empty method in your main app class.

"""
from typing import Any
from functools import partial

from kivy.app import App                                                            # type: ignore
from kivy.lang import Builder                                                       # type: ignore
from kivy.properties import StringProperty                                          # type: ignore

from ae.gui_app import id_of_flow, register_package_images                          # type: ignore
from ae.kivy.widgets import FlowButton, FlowDropDown                                # type: ignore
from ae.kivy.i18n import get_txt                                                    # type: ignore


__version__ = '0.3.32'


register_package_images()


Builder.load_string("""\
#: import _i_ ae.kivy_iterable_displayer
#: import DEF_LANGUAGE ae.i18n.DEF_LANGUAGE
#: import INSTALLED_LANGUAGES ae.i18n.INSTALLED_LANGUAGES

#: import DEBUG_LEVELS ae.core.DEBUG_LEVELS

#: import THEME_DARK_BACKGROUND_COLOR ae.gui_app.THEME_DARK_BACKGROUND_COLOR
#: import THEME_DARK_FONT_COLOR ae.gui_app.THEME_DARK_FONT_COLOR
#: import THEME_LIGHT_BACKGROUND_COLOR ae.gui_app.THEME_LIGHT_BACKGROUND_COLOR
#: import THEME_LIGHT_FONT_COLOR ae.gui_app.THEME_LIGHT_FONT_COLOR


<UserPreferencesButton@FlowButton>
    tap_flow_id: id_of_flow('open', 'user_preferences')
    ellipse_fill_ink: app.mixed_back_ink

<UserPreferencesPopup@FlowDropDown>
    canvas.before:
        Color:
            rgba: app.mixed_back_ink
        RoundedRectangle:
            pos: self.pos
            size: self.size
    FlowButton:
        tap_flow_id: id_of_flow('open', 'themes_menu')
        text: _("themes")
        square_fill_ink: Window.clearcolor
    FlowButton:
        tap_flow_id: id_of_flow('open', 'colors_menu')
        text: _("colors")
        square_fill_ink: Window.clearcolor
    AppStateSlider:
        app_state_name: 'sound_volume'
        cursor_image: 'atlas://data/images/defaulttheme/audio-volume-high'
        min: 0.0
        max: 1.0
        step: 0.03
    AppStateSlider:    # current kivy module vibrator.py does not support amplitudes arg of android api
        app_state_name: 'vibration_volume'
        cursor_image: app.main_app.img_file('vibration', app.app_states['font_size'], app.app_states['light_theme'])
        min: 0.0
        max: 1.0
        step: 0.1
    AppStateSlider:
        app_state_name: 'font_size'
        cursor_image: app.main_app.img_file('font_size', app.app_states['font_size'], app.app_states['light_theme'])
        min: app.min_font_size
        max: app.max_font_size
        step: 1
    BoxLayout:
        size_hint_y: None
        height: app.button_height if INSTALLED_LANGUAGES else 0
        opacity: 1 if INSTALLED_LANGUAGES else 0
        OptionalButton:
            lang_code: DEF_LANGUAGE
            tap_flow_id: id_of_flow('change', 'lang_code', self.lang_code)
            tap_kwargs: dict(popups_to_close=(root, ))
            square_fill_ink:
                app.app_states['update_ink'] if app.main_app.lang_code in ('', self.lang_code) else Window.clearcolor
            text: _(self.lang_code)
            visible: DEF_LANGUAGE not in INSTALLED_LANGUAGES
        LangCodeButton:
            lang_idx: 0
        LangCodeButton:
            lang_idx: 1
        LangCodeButton:
            lang_idx: 2
    BoxLayout:
        size_hint_y: None
        height: app.button_height
        FlowButton:
            tap_flow_id: id_of_flow('change', 'light_theme')
            tap_kwargs: dict(light_theme=False)
            text: _("dark")
            color: THEME_DARK_FONT_COLOR or self.color
            square_fill_ink: THEME_DARK_BACKGROUND_COLOR or self.square_fill_ink
        FlowButton:
            tap_flow_id: id_of_flow('change', 'light_theme')
            tap_kwargs: dict(light_theme=True)
            text: _("light")
            color: THEME_LIGHT_FONT_COLOR or self.color
            square_fill_ink: THEME_LIGHT_BACKGROUND_COLOR or self.square_fill_ink
    BoxLayout:
        size_hint_y: None
        height: app.button_height if app.main_app.debug else 0
        opacity: 1 if app.main_app.debug else 0
        DebugLevelButton:
            level_idx: 0
        DebugLevelButton:
            level_idx: 1
        DebugLevelButton:
            level_idx: 2
        DebugLevelButton:
            level_idx: 3
    BoxLayout:
        size_hint_y: None
        height: app.button_height if app.main_app.debug else 0
        opacity: 1 if app.main_app.debug else 0
        KbdInputModeButton:
            text: 'below_target'
        KbdInputModeButton:
            text: 'pan'
        KbdInputModeButton:
            text: 'scale'
        KbdInputModeButton:
            text: 'resize'
        KbdInputModeButton:
            text: ''
    OptionalButton:
        size_hint_x: 1
        text: "kivy settings"
        visible: app.main_app.verbose
        on_release: app.open_settings()
    OptionalButton:
        tap_flow_id: id_of_flow('open', 'iterable_displayer', 'app env info')
        tap_kwargs: dict(popup_kwargs=dict(title=self.text, data=app.main_app.app_env_dict()))
        size_hint_x: 1
        text: "app and system info"
        visible: app.main_app.debug
    OptionalButton:
        tap_flow_id: id_of_flow('open', 'f_string_evaluator')
        tap_kwargs: dict(popup_kwargs=dict(title=self.text))
        size_hint_x: 1
        text: "help message f-string evaluator"
        visible: app.main_app.debug
    OptionalButton:
        size_hint_x: 1
        text: "backup configs/resources"
        visible: app.main_app.debug
        on_release:
            app.main_app.show_message("at: " + app.main_app.backup_config_resources(), title="cfg/res backup stored"); \
            root.close()
    OptionalButton:
        tap_flow_id: id_of_flow('import', 'credentials')    # event handler implemented in :mod:`ae.kivy.apps` module
        size_hint_x: 1
        text: "import credentials from clipboard"
        visible: app.main_app.debug and hasattr(app.main_app, 'on_credentials_import')


<ColorsMenuPopup@FlowDropDown>
    child_data_maps: [dict(cls='ChangeColorButton', kwargs=dict(color_name=_c)) for _c in app.main_app.color_attr_names]

<ChangeColorButton>
    tap_flow_id: id_of_flow('open', 'color_editor', self.color_name)
    square_fill_ink: Window.clearcolor
    ellipse_fill_ink: app.app_states[self.color_name]
    text: _(self.color_name)

<ColorEditorPopup@FlowDropDown>
    auto_width_anim_duration: 0.3
    fully_opened: False
    on_complete_opened: self.fully_opened = True; color_editor.color = app.app_states[root.attach_to.color_name]
    ColorPicker:
        id: color_editor
        on_color:
            root.fully_opened and root.attach_to and \
            app.main_app.change_app_state(root.attach_to.color_name, list(args[1]))
        size_hint_y: None
        height: self.width
        canvas.before:
            Color:
                rgba: Window.clearcolor
            RoundedRectangle:
                pos: self.pos
                size: self.size


<ThemesMenuPopup>
    child_data_maps: self.child_menu_items(app.app_states['theme_names'])


<LangCodeButton@OptionalButton>
    lang_idx: 0
    lang_code: INSTALLED_LANGUAGES[min(self.lang_idx, len(INSTALLED_LANGUAGES) - 1)]
    tap_flow_id: id_of_flow('change', 'lang_code', self.lang_code)
    tap_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_ink: app.app_states['read_ink'] if app.main_app.lang_code == self.lang_code else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    text: _(self.lang_code)
    visible: len(INSTALLED_LANGUAGES) > self.lang_idx

<DebugLevelButton@OptionalButton>
    level_idx: 0
    tap_flow_id: id_of_flow('change', 'debug_level', self.text)
    tap_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_ink: app.app_states['read_ink'] if app.main_app.debug_level == self.level_idx else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    text: DEBUG_LEVELS[min(self.level_idx, len(DEBUG_LEVELS) - 1)]
    visible: app.main_app.debug and self.level_idx < len(DEBUG_LEVELS)

<KbdInputModeButton@OptionalButton>
    tap_flow_id: id_of_flow('change', 'kbd_input_mode', self.text)
    tap_kwargs: dict(popups_to_close=(self.parent.parent.parent, ))
    square_fill_ink: app.app_states['read_ink'] if app.main_app.kbd_input_mode == self.text else Window.clearcolor
    size_hint_x: 1 if self.visible else None
    visible: app.main_app.debug

<FStringEvaluatorPopup@FlowPopup>
    BoxLayout:
        orientation: 'vertical'
        FlowInput:
            id: eval_text
            size_hint_y: None
            height: app.main_app.font_size * 1.8
            focus: True
            auto_complete_texts: file_lines(normalize("{ado}/FStringEvalSuggestions.txt"))
            on_auto_complete_texts:
                write_file_text(self.auto_complete_texts, normalize("{ado}/FStringEvalSuggestions.txt"))
            on_text_validate:
                result_label.text = str(_(eval_text.text, \
                glo_vars=app.main_app.global_variables(evaluator_popup=root, input_widget=self)))
        FlowButton:
            text: "evaluate '" + eval_text.text + "'"
            size_hint_y: None
            height: app.button_height
            square_fill_ink: app.app_states['read_ink']
            on_release:
                result_label.text = str(_(eval_text.text, \
                glo_vars=app.main_app.global_variables(evaluator_popup=root, tap_widget=self)))
        ScrollView:
            always_overscroll: False        # workaround to kivy scrollview bug (viewport kept at bottom)
            do_scroll_x: False
            Label:
                id: result_label
                text_size: self.width, None
                size_hint: 1, None
                height: self.texture_size[1]
                color: app.font_color
                font_size: app.main_app.font_size * 0.75
""")


class ChangeColorButton(FlowButton):
    """ button widget created for each color. """
    color_name = StringProperty()           #: name of the color to change


class ThemesMenuPopup(FlowDropDown):
    """ menu popup for the app themes with dynamic menu items for each theme. """
    @staticmethod
    def child_menu_items(theme_names: list[str]) -> list[dict[str, Any]]:       # pragma: no cover
        """ return child_data_maps list of menu item widget instantiation kwargs for the specified theme names.

        :param theme_names:     theme names (app state) bound to trigger/update child_data_maps.
        :return:                menu item widget instantiation kwargs list.
        """
        main_app = App.get_running_app().main_app
        show_confirmation = main_app.show_confirmation
        add_theme_text = get_txt("save as theme")

        def _confirm(*_args, theme_id: str):  # function needed to theme_name value from within (and not after) loop
            show_confirmation(
                message=get_txt("delete app theme {theme_id}"),
                title="delete theme",
                confirm_flow_id=id_of_flow('delete', 'theme', theme_id))

        max_text_len = len(add_theme_text)
        mnu_items: list[dict[str, Any]] = []

        for theme_name in theme_names:
            max_text_len = max(max_text_len, len(theme_name))
            mnu_items.append(dict(kwargs=dict(
                text=theme_name,
                tap_flow_id=id_of_flow('change', 'theme', theme_name),
                on_alt_tap=partial(_confirm, theme_id=theme_name))))

        if mnu_items:
            mnu_items.append(dict(cls='ImageLabel', kwargs=dict(text="-" * max_text_len)))

        mnu_items.append(dict(kwargs=dict(
            text=add_theme_text,
            tap_flow_id=id_of_flow('show', 'input'),
            tap_kwargs=dict(
                popup_kwargs=dict(
                    message=get_txt("enter app theme name/id"),
                    title=add_theme_text,
                    confirm_flow_id=id_of_flow('save', 'theme'),
                    confirm_text=get_txt("save"),
                    input_default=main_app.theme_names[0] if main_app.theme_names else "",
                )
            )
        )))

        return mnu_items
