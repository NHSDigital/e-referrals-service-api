// eslint.config.js

const { configs } = require('@eslint/js');
const globals = require('globals');

module.exports = [
    configs.recommended,
	{
		languageOptions: {
			ecmaVersion: 2018,
			globals: {
				...globals.commonjs,
				...globals.es6,
				...globals.node,
				Atomics: "readonly",
				SharedArrayBuffer: "readonly",
			},
		},
		rules: {
		},
	},
]
