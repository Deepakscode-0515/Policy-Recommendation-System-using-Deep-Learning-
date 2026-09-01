TemplateAssertionError
jinja2.exceptions.TemplateAssertionError: No filter named 'loadjson'.

Traceback (most recent call last)
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 1488, in __call__
    ) -> cabc.Iterable[bytes]:
        """The WSGI server calls the Flask application object as the
        WSGI application. This calls :meth:`wsgi_app`, which can be
        wrapped to apply middleware.
        """
        return self.wsgi_app(environ, start_response)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 1466, in wsgi_app
            try:
                ctx.push()
                response = self.full_dispatch_request()
            except Exception as e:
                error = e
                response = self.handle_exception(e)
                           ^^^^^^^^^^^^^^^^^^^^^^^^
            except:  # noqa: B001
                error = sys.exc_info()[1]
                raise
            return response(environ, start_response)
        finally:
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 1463, in wsgi_app
        ctx = self.request_context(environ)
        error: BaseException | None = None
        try:
            try:
                ctx.push()
                response = self.full_dispatch_request()
                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            except Exception as e:
                error = e
                response = self.handle_exception(e)
            except:  # noqa: B001
                error = sys.exc_info()[1]
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 872, in full_dispatch_request
            request_started.send(self, _async_wrapper=self.ensure_sync)
            rv = self.preprocess_request()
            if rv is None:
                rv = self.dispatch_request()
        except Exception as e:
            rv = self.handle_user_exception(e)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        return self.finalize_request(rv)
 
    def finalize_request(
        self,
        rv: ft.ResponseReturnValue | HTTPException,
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 870, in full_dispatch_request
 
        try:
            request_started.send(self, _async_wrapper=self.ensure_sync)
            rv = self.preprocess_request()
            if rv is None:
                rv = self.dispatch_request()
                     ^^^^^^^^^^^^^^^^^^^^^^^
        except Exception as e:
            rv = self.handle_user_exception(e)
        return self.finalize_request(rv)
 
    def finalize_request(
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 855, in dispatch_request
            and req.method == "OPTIONS"
        ):
            return self.make_default_options_response()
        # otherwise dispatch to the handler for that endpoint
        view_args: dict[str, t.Any] = req.view_args  # type: ignore[assignment]
        return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
    def full_dispatch_request(self) -> Response:
        """Dispatches the request and on top of that performs request
        pre and postprocessing as well as HTTP exception catching and
        error handling.
File "C:\Users\Bhargav\Downloads\raf-flask\app.py", line 40, in index
@app.route("/")
def index():
    if current_user.is_authenticated:
        # Recent assessments for dashboard
        recent = Assessment.query.filter_by(user_id=current_user.id).order_by(Assessment.created_at.desc()).limit(5).all()
        return render_template("dashboard.html", recent=recent)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    return render_template("landing.html")
 
# Auth
@app.route("/register", methods=["GET", "POST"])
def register():
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\templating.py", line 149, in render_template
    :param template_name_or_list: The name of the template to render. If
        a list is given, the first name to exist will be rendered.
    :param context: The variables to make available in the template.
    """
    app = current_app._get_current_object()  # type: ignore[attr-defined]
    template = app.jinja_env.get_or_select_template(template_name_or_list)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    return _render(app, template, context)
 
 
def render_template_string(source: str, **context: t.Any) -> str:
    """Render a template from the given source string with the given
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\environment.py", line 1084, in get_or_select_template
        is given, or :meth:`get_template` if one name is given.
 
        .. versionadded:: 2.3
        """
        if isinstance(template_name_or_list, (str, Undefined)):
            return self.get_template(template_name_or_list, parent, globals)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        elif isinstance(template_name_or_list, Template):
            return template_name_or_list
        return self.select_template(template_name_or_list, parent, globals)
 
    def from_string(
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\environment.py", line 1013, in get_template
        if isinstance(name, Template):
            return name
        if parent is not None:
            name = self.join_path(name, parent)
 
        return self._load_template(name, globals)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
    @internalcode
    def select_template(
        self,
        names: t.Iterable[t.Union[str, "Template"]],
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\environment.py", line 972, in _load_template
                if globals:
                    template.globals.update(globals)
 
                return template
 
        template = self.loader.load(self, name, self.make_globals(globals))
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
        if self.cache is not None:
            self.cache[cache_key] = template
        return template
 
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\loaders.py", line 138, in load
            code = bucket.code
 
        # if we don't have code so far (not cached, no longer up to
        # date) etc. we compile the template
        if code is None:
            code = environment.compile(source, name, filename)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
        # if the bytecode cache is available and the bucket doesn't
        # have a code so far, we give the bucket the new code and put
        # it back to the bytecode cache.
        if bcc is not None and bucket.code is None:
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\environment.py", line 768, in compile
                return source
            if filename is None:
                filename = "<template>"
            return self._compile(source, filename)
        except TemplateSyntaxError:
            self.handle_exception(source=source_hint)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
    def compile_expression(
        self, source: str, undefined_to_none: bool = True
    ) -> "TemplateExpression":
        """A handy helper method that returns a callable that accepts keyword
File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\environment.py", line 939, in handle_exception
        """Exception handling helper.  This is used internally to either raise
        rewritten exceptions or return a rendered traceback for the template.
        """
        from .debug import rewrite_traceback_stack
 
        raise rewrite_traceback_stack(source=source)
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
    def join_path(self, template: str, parent: str) -> str:
        """Join a template with the parent.  By default all the lookups are
        relative to the loader root so this method returns the `template`
        parameter unchanged, but if the paths should be relative to the
File "C:\Users\Bhargav\Downloads\raf-flask\templates\dashboard.html", line 13, in template
    <h3>Recent Activity</h3>
    {% if recent %}
      <ul class="list">
        {% for r in recent %}
          {% set out = r.output_json | safe %}
          {% set parsed = out | loadjson %}
          <li class="card">
            <div class="row between">
              <strong>Assessment #{{ r.id }}</strong>
              <small>{{ r.created_at.strftime("%Y-%m-%d %H:%M") }}</small>
            </div>
jinja2.exceptions.TemplateAssertionError: No filter named 'loadjson'.
This is the Copy/Paste friendly version of the traceback.

Traceback (most recent call last):
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 1488, in __call__
    return self.wsgi_app(environ, start_response)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 1466, in wsgi_app
    response = self.handle_exception(e)
               ^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 1463, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 872, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 870, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\app.py", line 855, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\Downloads\raf-flask\app.py", line 40, in index
    return render_template("dashboard.html", recent=recent)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\flask\templating.py", line 149, in render_template
    template = app.jinja_env.get_or_select_template(template_name_or_list)
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\environment.py", line 1084, in get_or_select_template
    return self.get_template(template_name_or_list, parent, globals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\environment.py", line 1013, in get_template
    return self._load_template(name, globals)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\environment.py", line 972, in _load_template
    template = self.loader.load(self, name, self.make_globals(globals))
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\loaders.py", line 138, in load
    code = environment.compile(source, name, filename)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\environment.py", line 768, in compile
    self.handle_exception(source=source_hint)
  File "C:\Users\Bhargav\AppData\Roaming\Python\Python312\site-packages\jinja2\environment.py", line 939, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "C:\Users\Bhargav\Downloads\raf-flask\templates\dashboard.html", line 13, in template
    {% set parsed = out | loadjson %}
jinja2.exceptions.TemplateAssertionError: No filter named 'loadjson'.

The debugger caught an exception in your WSGI application. You can now look at the traceback which led to the error. If you enable JavaScript you can also use additional features such as code execution (if the evalex feature is enabled), automatic pasting of the exceptions and much more.
Brought to you by DON'T PANIC, your friendly Werkzeug powered traceback interpreter.