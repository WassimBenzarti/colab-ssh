# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Improve verbose output and increasing sleep times (@bjourne)
- When cloning private repositories, the message "Cloned the repo successfully" doesn't show up anymore.
- Check if the repository is public, before cloning it.
- Ask for password if the repository is private (in other words not found in the remote)
- Add the appropriate documentation
- Continue integrating `pytest` for better test development and readability

## v0.2.61 - 2020-09-01
- Add warning for uses in other notebooks (in other platforms)
- Add support for passwords. If the repository is private, you will be asked to enter your login username and password.
- Improve the errors related to branches
- Add support for a reserved remote address (issue opened by @rbracco) 

- Fix issues with git URL extension thanks to @flych3r
- Add more required environment variables (by @bjourne), fixes #18.
- Improve the way we get the public_url, to avoid unexpected errors
- Add a link to open VSCode directly when calling init_git
- Fix some bugs
