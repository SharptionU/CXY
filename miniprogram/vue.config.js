module.exports = {
  css: {
    loaderOptions: {
      sass: {
        // 全局注入的 SCSS 文件（注意分号分隔）
        additionalData: `
          @import "@/styles/theme.scss";
        `
      }
    }
  }
};