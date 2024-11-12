module.exports = {
  css: {
    loaderOptions: {
      postcss: {
        postcssOptions: {  // 将 plugins 移入 postcssOptions
          plugins: [
            require('postcss-pxtorem')({
              rootValue: 16,
              propList: ['*']
            }),
          ],
        },
      },
    },
  },
};
