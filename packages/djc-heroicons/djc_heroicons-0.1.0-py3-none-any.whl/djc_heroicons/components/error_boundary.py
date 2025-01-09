from typing import Dict, Optional, Union

from django.template import Context, TemplateSyntaxError
from django.utils.safestring import SafeString, mark_safe
from django_components import Component, types


# TODO - Add once validation in django-components is fixed
#
# class ErrorBoundaryKwargs(TypedDict):
#     fallback: NotRequired[Union[type[Component], str, SafeString]]
#     params: NotRequired[Dict]
# ErrorBoundaryType = Component[EmptyTuple, ErrorBoundaryKwargs, EmptyDict, Any, Any, Any]


DEFAULT_FALLBACK = mark_safe("""
    <div>
        <h1>Something went wrong!</h1>
        <p>Please try again.</p>
    </div>
""")


# TODO - ADD SETTING TO OVERRIDE DEFAULT FALLBACK
# TODO - ADD SETTING TO DISABLE ERROR BOUNDARY IN DEBUG MODE
# TODO - BASED ON https://github.com/dillonchanis/vue-error-boundary
#        SEE https://github.com/dillonchanis/vue-error-boundary/blob/main/src/VErrorBoundary.vue
# TODO - FOR DOCUMENTATION INSPO, SEE https://legacy.reactjs.org/blog/2017/07/26/error-handling-in-react-16.html
class ErrorBoundary(Component):
    def get_context_data(
        self,
        /,
        *,
        fallback: Optional[Union[type[Component], str, SafeString]] = None,
        params: Optional[Dict] = None,
    ) -> Dict:
        fallback_slot = self.input.slots.get("fallback", None)
        if fallback_slot and fallback:
            raise ValueError("ErrorBoundary component cannot have both a fallback slot and a fallback kwarg")

        return {
            "fallback": fallback,
            "params": params,
        }

    def on_render(self, context: Context) -> SafeString:
        content_slot = self.input.slots.get("default", None)
        if not content_slot:
            raise TemplateSyntaxError("ErrorBoundary component must the 'default' slot")

        try:
            return content_slot(context)
        except Exception as err:
            fallback_slot = self.input.slots.get("fallback", None)
            fallback = self.input.kwargs.get("fallback", None)

            if fallback_slot:
                return fallback_slot(context)

            elif fallback:
                # Fallback kwarg may be a component or a string
                if issubclass(fallback, Component):
                    params = (self.input.kwargs.get("params", None) or {}).copy()
                    params["error"] = err
                    return fallback.render(
                        kwargs=params,
                    )
                else:
                    return fallback
            else:
                return DEFAULT_FALLBACK
