def make_exe():
    dist = default_python_distribution(python_version="3.10")

    policy = dist.make_python_packaging_policy()
    policy.set_resource_handling_mode("files")

    # site-packages is required here so that streamlit doesn't boot in
    # development mode:
    # https://github.com/streamlit/streamlit/blob/953dfdbe/lib/streamlit/config.py#L255-L267
    policy.resources_location = "filesystem-relative:site-packages"

    python_config = dist.make_python_interpreter_config()
    python_config.module_search_paths = ["$ORIGIN/site-packages"]
    python_config.run_module = "scholarship_app"

    python_config.filesystem_importer = True
    python_config.oxidized_importer = False
    python_config.sys_frozen = True

    exe = dist.to_python_executable(
        name="uiowa-scholarship-tool",
        packaging_policy=policy,
        config=python_config,
    )
    exe.windows_runtime_dlls_mode = "always"
    exe.windows_subsystem = "console"

    exe.add_python_resources(exe.pip_install(["-r", "requirements.txt"]))
    exe.add_python_resources(exe.pip_install(["."]))

    return exe

def make_install(exe):
    files = FileManifest()
    files.add_python_resource(".", exe)

    # Save executable
    files.install("dist", replace=True)

    # MacOS Bundle Build
    bundle_builder = MacOsApplicationBundleBuilder('uiowa-scholarship-tool')
    bundle_builder.add_manifest(files)
    bundle_builder.set_info_plist_required_keys('scholarship', 'edu.uiowa.engineering.scholarship_app', '1.0', 'usat', 'uiowa-scholarship-tool')
    bundle_builder.build("dist")
    bundle_builder.write_to_directory("dist")

    #apple_binary = AppleUniversalBinary('scholarship')

    return files

register_target("exe", make_exe)
register_target(
    "install", make_install, depends=["exe"], default=True, default_build_script=True
)

resolve_targets()
