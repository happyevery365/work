module.exports = {
  parserOptions: {
    parser: '@babel/eslint-parser',
    ecmaVersion: 2020,
    sourceType: 'module',
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-essential',
  ],
  rules: {
    'no-undef': 'off',  // 关闭对 defineProps 的检查
  }
}
