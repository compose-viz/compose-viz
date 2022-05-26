<div id="top"></div>

<!-- PROJECT SHIELDS -->

[<div align="center"> ![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![MIT License][license-shield]][license-url]
[![Issues][issues-shield]][issues-url]
[![Issues Closed][issues-closed-shield]</div>][issues-closed-url]

<br />

<!-- PROJECT LOGO -->

![compose-viz](https://socialify.git.ci/compose-viz/compose-viz/image?description=1&font=KoHo&name=1&owner=1&pattern=Circuit%20Board&theme=Light)

<br />
<div align="center">
<p align="center">
    <a href="https://github.com/compose-viz/compose-viz#usage"><strong>Explore Usage »</strong></a>
    <br />
    <br />
    <a href="https://github.com/compose-viz/compose-viz/issues">Report Bug</a>
    ·
    <a href="https://github.com/compose-viz/compose-viz/issues">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisities">Prerequisities</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#example">Example</a></li>
        <li><a href="#usage">Usage</a></li>
        <li><a href="#options">Options</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

`compose-viz` is a compose file visualization tool that supports [compose-spec](https://github.com/compose-spec/compose-spec/blob/master/spec.md) and allows you to gernerate graph in several formats.

If you are looking for a compose file vizualization tool, and you are using one of the [compose-spec](https://github.com/compose-spec/compose-spec/blob/master/spec.md) implementations (e.g. [docker-compose](https://github.com/docker/compose)/[podman-compose](https://github.com/containers/podman-compose)), then `compose-viz` is a great choice for you. 

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisities

#### Graphviz

You need to install [Graphviz](https://graphviz.org/download/) to generate graphs.

### Installation

#### Using `pip`

`pip install compose-viz`

#### Using `.whl`

See [releases](https://github.com/compose-viz/compose-viz/releases).

### Example

This example yml is from [docker compose beginner tutorial](https://github.com/docker/labs/blob/master/beginner/chapters/votingapp.md).

```bash
cd examples/voting-app/
cpv -m svg docker-compose.yml
```

And this is what the result looks like:

![compose-viz.svg](https://github.com/compose-viz/compose-viz/blob/main/examples/voting-app/compose-viz.svg)

Check out the result [here](https://github.com/compose-viz/compose-viz/blob/main/examples/voting-app).

### Usage

`cpv [OPTIONS] INPUT_PATH`

### Options

| Option                         | Description                                                                                                                                                                  |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-o, --output-filename` | Output filename for the generated visualization file. [default: compose-viz]                                                                                          |
| `-m, --format`                 | Output format for the generated visualization file. See [supported formats](https://github.com/compose-viz/compose-viz/blob/main/compose_viz/viz_formats.py). [default: png] |
| `-v, --version`                | Show the version of compose-viz.                                                                                                                                             |
| `--help`                       | Show help and exit.                                                                                                                                                          |

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

- [ ] Support more vizualization components.

See the [open issues](https://github.com/compose-viz/compose-viz/issues)
for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to
learn, inspire, and create. Any contributions you make are **greatly
appreciated**.

If you have a suggestion that would make this better, please fork the repo and
create a pull request. You can also simply open an issue with the tag
"enhancement". Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feat/amazing-feature`)
3. Commit your Changes with
   [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
4. Push to the Branch (`git push origin feat/amazing-feature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See
[LICENSE](https://github.com/compose-viz/compose-viz/blob/main/LICENSE)
for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

### Author

- HSING-HAN, WU (Xyphuz)
  - Mail me: xyphuzwu@gmail.com
  - About me: <https://about.xyphuz.com>
  - GitHub: <https://github.com/wst24365888>

### Project Link

- <https://github.com/compose-viz/compose-viz>

<p align="right">(<a href="#top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/compose-viz/compose-viz.svg?style=for-the-badge
[contributors-url]: https://github.com/compose-viz/compose-viz/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/compose-viz/compose-viz.svg?style=for-the-badge
[forks-url]: https://github.com/compose-viz/compose-viz/network/members
[stars-shield]: https://img.shields.io/github/stars/compose-viz/compose-viz.svg?style=for-the-badge
[stars-url]: https://github.com/compose-viz/compose-viz/stargazers
[issues-shield]: https://img.shields.io/github/issues/compose-viz/compose-viz.svg?style=for-the-badge
[issues-url]: https://github.com/compose-viz/compose-viz/issues
[issues-closed-shield]: https://img.shields.io/github/issues-closed/compose-viz/compose-viz.svg?style=for-the-badge
[issues-closed-url]: https://github.com/compose-viz/compose-viz/issues?q=is%3Aissue+is%3Aclosed
[license-shield]: https://img.shields.io/github/license/compose-viz/compose-viz.svg?style=for-the-badge
[license-url]: https://github.com/compose-viz/compose-viz/blob/main/LICENSE