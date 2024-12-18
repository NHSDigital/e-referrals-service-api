/**
 * @file validationUtil.js
 * @description Provides utility functions.
 */

function isValidUuid(string) {
    return /^[0-9A-F]{8}-[0-9A-F]{4}-[4][0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$/i.test(string);
  }

function hasLegacyPrefix(string) {
    return string.startsWith('att-');
}

module.exports = {
    isValidUuid,
    hasLegacyPrefix,
};