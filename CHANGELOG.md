# Change Log

The change log has moved to this repo's [GitHub Releases Page](https://github.com/rollbar/rollbar-agent/releases).
**0.4.4**
- Improve error handling: See [#50](https://github.com/rollbar/rollbar-agent/pull/50)

**0.4.3**
- add content-type: application/json to post request [#39](https://github.com/rollbar/rollbar-agent/pull/39)
- Support multiple spaces in in log_format.patterns [#38](https://github.com/rollbar/rollbar-agent/pull/38)
- Add option to filter character attribute modifying terminal escape sequences [#36](https://github.com/rollbar/rollbar-agent/pull/36)

**0.4.1**
- Improve internal error handling. See [#35](https://github.com/rollbar/rollbar-agent/pull/35)

**0.4.0**
- Fix a few installation issues, and bump minor version.

**0.3.12**
- Fix a bug introduced by the delete files option. See [#23](https://github.com/rollbar/rollbar-agent/pull/23)

**0.3.11**
- Add option to delete files once they are fully processed. See [#22](https://github.com/rollbar/rollbar-agent/pull/22)

**0.3.10**
- Fix a bug where we weren't releasing the state file before recreating it. See [#17](https://github.com/rollbar/rollbar-agent/issues/17)

**0.3.9**
- Fall back to rollbar-agent's access token if a loaded item payload doesn't contain one

**0.3.8**
- Properly clean up state file when log files are deleted

**0.3.7**
- Fix issues when payloads contain unicode

**0.3.6**
- Output a helpful error message if the configuration file isn't found on load

**0.3.5**
- Allow configurable log levels to be defined

**0.3.4**
- Added 'warn' log level

**0.3.1**
- Added skip_to_end option. "Go through existing log files and save them in the state without processing them, so you do not process existing log info next run. Exits after processing once."
