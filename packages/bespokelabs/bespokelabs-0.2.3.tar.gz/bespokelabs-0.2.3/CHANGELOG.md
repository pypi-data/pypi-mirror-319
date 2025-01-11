# Changelog

## 0.2.3 (2025-01-09)

Full Changelog: [v0.2.2...v0.2.3](https://github.com/bespokelabsai/bespokelabs-python/compare/v0.2.2...v0.2.3)

### Bug Fixes

* **client:** only call .close() when needed ([#44](https://github.com/bespokelabsai/bespokelabs-python/issues/44)) ([ea2bd4e](https://github.com/bespokelabsai/bespokelabs-python/commit/ea2bd4eea5b94df8223bb47369f35449637b8f05))


### Chores

* **internal:** bump httpx dependency ([#43](https://github.com/bespokelabsai/bespokelabs-python/issues/43)) ([b4224bd](https://github.com/bespokelabsai/bespokelabs-python/commit/b4224bd9ed1ac45bc2c44c5322b885f9936ef4c9))
* **internal:** codegen related update ([#41](https://github.com/bespokelabsai/bespokelabs-python/issues/41)) ([e2f9c92](https://github.com/bespokelabsai/bespokelabs-python/commit/e2f9c92f68034ac50ea5f8ba94ab4017af88b60f))
* **internal:** codegen related update ([#46](https://github.com/bespokelabsai/bespokelabs-python/issues/46)) ([209d865](https://github.com/bespokelabsai/bespokelabs-python/commit/209d8658c61592da6409b8cc14a5f1e56f4f31b0))

## 0.2.2 (2024-12-18)

Full Changelog: [v0.2.1...v0.2.2](https://github.com/bespokelabsai/bespokelabs-python/compare/v0.2.1...v0.2.2)

### Chores

* **internal:** codegen related update ([#34](https://github.com/bespokelabsai/bespokelabs-python/issues/34)) ([42d20f2](https://github.com/bespokelabsai/bespokelabs-python/commit/42d20f2c5dbd702f8dd5c7527077dd8bbd25ff60))
* **internal:** codegen related update ([#36](https://github.com/bespokelabsai/bespokelabs-python/issues/36)) ([33c717e](https://github.com/bespokelabsai/bespokelabs-python/commit/33c717e6a5c4b9e48ba736ac8da580c4ba2b107f))
* **internal:** codegen related update ([#38](https://github.com/bespokelabsai/bespokelabs-python/issues/38)) ([9b182a3](https://github.com/bespokelabsai/bespokelabs-python/commit/9b182a3c9b37aa6c648e301b1b7dd23516bdba6b))
* **internal:** fix some typos ([#39](https://github.com/bespokelabsai/bespokelabs-python/issues/39)) ([3c46922](https://github.com/bespokelabsai/bespokelabs-python/commit/3c46922f5752524232cc69e4c5fb350145cb0ba5))
* **internal:** updated imports ([#37](https://github.com/bespokelabsai/bespokelabs-python/issues/37)) ([5f521c0](https://github.com/bespokelabsai/bespokelabs-python/commit/5f521c0a9246e17c58f1d9a4e1c7192651615bba))

## 0.2.1 (2024-12-13)

Full Changelog: [v0.2.0...v0.2.1](https://github.com/bespokelabsai/bespokelabs-python/compare/v0.2.0...v0.2.1)

### Chores

* **internal:** add support for TypeAliasType ([#32](https://github.com/bespokelabsai/bespokelabs-python/issues/32)) ([2b348b2](https://github.com/bespokelabsai/bespokelabs-python/commit/2b348b211e7bba1d4a96bad405b4a65ccc927705))
* **internal:** bump pyright ([#31](https://github.com/bespokelabsai/bespokelabs-python/issues/31)) ([96479d8](https://github.com/bespokelabsai/bespokelabs-python/commit/96479d8058d4665f65e5a72bae5a178023333a5a))
* **internal:** codegen related update ([#30](https://github.com/bespokelabsai/bespokelabs-python/issues/30)) ([5dd97d0](https://github.com/bespokelabsai/bespokelabs-python/commit/5dd97d0017c00888af7c3a332e627f85cd34cfae))
* make the `Omit` type public ([#28](https://github.com/bespokelabsai/bespokelabs-python/issues/28)) ([e6c8305](https://github.com/bespokelabsai/bespokelabs-python/commit/e6c8305b287a400bc63b8d40375363dc8f310850))

## 0.2.0 (2024-12-03)

Full Changelog: [v0.1.1...v0.2.0](https://github.com/bespokelabsai/bespokelabs-python/compare/v0.1.1...v0.2.0)

### Features

* **api:** api update ([#11](https://github.com/bespokelabsai/bespokelabs-python/issues/11)) ([6b7d04c](https://github.com/bespokelabsai/bespokelabs-python/commit/6b7d04c370a723783df80c09f267053ca71edaf5))


### Bug Fixes

* **client:** compat with new httpx 0.28.0 release ([#25](https://github.com/bespokelabsai/bespokelabs-python/issues/25)) ([a136025](https://github.com/bespokelabsai/bespokelabs-python/commit/a136025df0b967d2d187efcf37a7cd8434d82191))


### Chores

* **internal:** bump pyright ([#26](https://github.com/bespokelabsai/bespokelabs-python/issues/26)) ([9b799e0](https://github.com/bespokelabsai/bespokelabs-python/commit/9b799e0d08cbb1a654964feccb5c32e2a71f1650))
* **internal:** exclude mypy from running on tests ([#24](https://github.com/bespokelabsai/bespokelabs-python/issues/24)) ([09ac45c](https://github.com/bespokelabsai/bespokelabs-python/commit/09ac45c89cd7cbd22124828cd78deb7c4c991a6b))
* **internal:** fix compat model_dump method when warnings are passed ([#21](https://github.com/bespokelabsai/bespokelabs-python/issues/21)) ([bc70cb2](https://github.com/bespokelabsai/bespokelabs-python/commit/bc70cb2cfde0d63e7255e0870114ca5bc4f7f52c))
* rebuild project due to codegen change ([#13](https://github.com/bespokelabsai/bespokelabs-python/issues/13)) ([f0f4e01](https://github.com/bespokelabsai/bespokelabs-python/commit/f0f4e01ea78c3afe2ed086e98ff6d9eced208fe2))
* rebuild project due to codegen change ([#14](https://github.com/bespokelabsai/bespokelabs-python/issues/14)) ([4d1b00a](https://github.com/bespokelabsai/bespokelabs-python/commit/4d1b00ab32c0e9e69b44942781d0a1e994dc51b3))
* rebuild project due to codegen change ([#15](https://github.com/bespokelabsai/bespokelabs-python/issues/15)) ([16a313e](https://github.com/bespokelabsai/bespokelabs-python/commit/16a313ee5b0ed49d70fb8240bdf3cd60d8a35b7e))
* rebuild project due to codegen change ([#16](https://github.com/bespokelabsai/bespokelabs-python/issues/16)) ([22ca99d](https://github.com/bespokelabsai/bespokelabs-python/commit/22ca99d2b5f38c431914ecf79389637c89c7e892))
* rebuild project due to codegen change ([#17](https://github.com/bespokelabsai/bespokelabs-python/issues/17)) ([739400f](https://github.com/bespokelabsai/bespokelabs-python/commit/739400f6a85165c7c0bc42a64c705c5ca03229c6))
* rebuild project due to codegen change ([#18](https://github.com/bespokelabsai/bespokelabs-python/issues/18)) ([c52a1db](https://github.com/bespokelabsai/bespokelabs-python/commit/c52a1dba63c3d58ba8e2efa00d28cbf5f062c06d))
* rebuild project due to codegen change ([#19](https://github.com/bespokelabsai/bespokelabs-python/issues/19)) ([f719642](https://github.com/bespokelabsai/bespokelabs-python/commit/f7196420739ecfd3b8fbcbe665ef98597fd704af))
* rebuild project due to codegen change ([#20](https://github.com/bespokelabsai/bespokelabs-python/issues/20)) ([ab615de](https://github.com/bespokelabsai/bespokelabs-python/commit/ab615de01029a6ea18e6691df04f57241ec4d54b))
* remove now unused `cached-property` dep ([#23](https://github.com/bespokelabsai/bespokelabs-python/issues/23)) ([3f2bfe0](https://github.com/bespokelabsai/bespokelabs-python/commit/3f2bfe0cf97cbf79760badc7273003976f65278a))


### Documentation

* add info log level to readme ([#22](https://github.com/bespokelabsai/bespokelabs-python/issues/22)) ([ea78b4d](https://github.com/bespokelabsai/bespokelabs-python/commit/ea78b4de7416e724beaac54e68ecd1d0e5678045))

## 0.1.1 (2024-09-05)

Full Changelog: [v0.1.0...v0.1.1](https://github.com/bespokelabsai/bespokelabs-python/compare/v0.1.0...v0.1.1)

### Features

* **api:** update via SDK Studio ([#7](https://github.com/bespokelabsai/bespokelabs-python/issues/7)) ([052e2ed](https://github.com/bespokelabsai/bespokelabs-python/commit/052e2ede8c634b31dc4075d57b88bfc7fdb9cb59))


### Chores

* pyproject.toml formatting changes ([#9](https://github.com/bespokelabsai/bespokelabs-python/issues/9)) ([0f5c6e8](https://github.com/bespokelabsai/bespokelabs-python/commit/0f5c6e84656c6b48640ffb4bbb47780e94a9ed4a))

## 0.1.0 (2024-09-04)

Full Changelog: [v0.1.0-alpha.1...v0.1.0](https://github.com/bespokelabsai/bespokelabs-python/compare/v0.1.0-alpha.1...v0.1.0)

### Features

* **api:** update via SDK Studio ([#4](https://github.com/bespokelabsai/bespokelabs-python/issues/4)) ([88ab107](https://github.com/bespokelabsai/bespokelabs-python/commit/88ab107c0b748171107610ca7996a7e7cd34cfc2))

## 0.1.0-alpha.1 (2024-09-04)

Full Changelog: [v0.0.1-alpha.0...v0.1.0-alpha.1](https://github.com/bespokelabsai/bespokelabs-python/compare/v0.0.1-alpha.0...v0.1.0-alpha.1)

### Features

* **api:** update via SDK Studio ([54053fb](https://github.com/bespokelabsai/bespokelabs-python/commit/54053fb6a75d481609d33102f198e3dc91b3ba60))
* **api:** update via SDK Studio ([7fe5a36](https://github.com/bespokelabsai/bespokelabs-python/commit/7fe5a367cd4ef0e6d06f960bcd49bf2845223326))
* **api:** update via SDK Studio ([cdcc900](https://github.com/bespokelabsai/bespokelabs-python/commit/cdcc900b8e9a37045889fd96199dc866b60c076d))
* **api:** update via SDK Studio ([003129a](https://github.com/bespokelabsai/bespokelabs-python/commit/003129a7672a76149ebaa139cdae241e296b1fcd))
* **api:** update via SDK Studio ([224b3c9](https://github.com/bespokelabsai/bespokelabs-python/commit/224b3c9a2751a732e1d1c9a3426caf6df0882960))
* **api:** update via SDK Studio ([85409ce](https://github.com/bespokelabsai/bespokelabs-python/commit/85409cebb1bea4e92d834374edfe16669a7a41eb))
* **api:** update via SDK Studio ([b0632a3](https://github.com/bespokelabsai/bespokelabs-python/commit/b0632a3db7f72e9556590d84aa744fe4a50b12af))


### Chores

* go live ([#1](https://github.com/bespokelabsai/bespokelabs-python/issues/1)) ([a01a998](https://github.com/bespokelabsai/bespokelabs-python/commit/a01a998870299ef7acf0432382b1868908da319e))
