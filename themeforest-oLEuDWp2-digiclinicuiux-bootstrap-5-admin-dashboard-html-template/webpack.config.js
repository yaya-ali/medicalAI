const Path = require("path");
const Webpack = require("webpack");
const TerserPlugin = require("terser-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const CopyWebpackPlugin = require("copy-webpack-plugin");
const FileManagerPlugin = require("filemanager-webpack-plugin");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const Handlebars = require("handlebars");

const opts = {
  rootDir: process.cwd(),
  devBuild: process.env.NODE_ENV !== "production"
};

module.exports = {
  // core directory
  entry: {
    'app': "./src/assets/js/app.js",
  },
  mode: process.env.NODE_ENV === "production" ? "production" : "development",
  devtool: process.env.NODE_ENV === "production" ? "source-map" : "inline-source-map",
  output: {
    path: Path.join(opts.rootDir, "dist"),
    pathinfo: opts.devBuild,
    filename: "assets/js/[name].js",
    chunkFilename: 'assets/js/[name].js',

  },
  performance: { hints: false },
  optimization: {
    minimizer: [
      new TerserPlugin({
        parallel: true,
        terserOptions: {
          ecma: 5
        }
      }),
      new CssMinimizerPlugin({})
    ],
    runtimeChunk: false
  },
  plugins: [
    // Extract css files to seperate bundle
    new MiniCssExtractPlugin({
      filename: "assets/css/app.css",
      chunkFilename: "assets/css/app.css"
    }),

    // Copy fonts and images to dist
    new CopyWebpackPlugin({
      patterns: [
        // images copy
        { from: "src/assets/img", to: "assets/img" },
        // page level scripts 
        { from: "src/assets/js/component", to: "assets/js/component" },
        { from: "src/assets/js/clinic", to: "assets/js/clinic" },
        // demo pages
        // { from: "src/pages", to: "" },
      ]
    }),

    new Webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    }),

    // blank
    new HtmlWebpackPlugin({ filename: "index.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/index.html", inject: true, hash: true, title: "Blank Page" }),
    new HtmlWebpackPlugin({ filename: "page-not-found.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/page-not-found.html", inject: true, hash: true, title: "Error 404" }),
    new HtmlWebpackPlugin({ filename: "page-not-found-2.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/page-not-found-2.html", inject: true, hash: true, title: "Error 404" }),
    new HtmlWebpackPlugin({ filename: "page-not-found-3.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/page-not-found-3.html", inject: true, hash: true, title: "Error 404" }),
    new HtmlWebpackPlugin({ filename: "under-construction.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/under-construction.html", inject: true, hash: true, title: "Under Construction" }),
    new HtmlWebpackPlugin({ filename: "coming-soon.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/coming-soon.html", inject: true, hash: true, title: "Coming Soon" }),

    // clinic 
    new HtmlWebpackPlugin({ filename: "clinic-aboutus.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-aboutus.html", inject: true, hash: true, title: "clinic-aboutus" }),
    new HtmlWebpackPlugin({ filename: "clinic-add-appointment.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-add-appointment.html", inject: true, hash: true, title: "clinic-add-appointment" }),
    new HtmlWebpackPlugin({ filename: "clinic-add-blog.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-add-blog.html", inject: true, hash: true, title: "clinic-add-blog" }),
    new HtmlWebpackPlugin({ filename: "clinic-add-invoice.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-add-invoice.html", inject: true, hash: true, title: "clinic-add-invoice" }),
    new HtmlWebpackPlugin({ filename: "clinic-add-patient.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-add-patient.html", inject: true, hash: true, title: "clinic-add-patient" }),
    new HtmlWebpackPlugin({ filename: "clinic-add-ticket.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-add-ticket.html", inject: true, hash: true, title: "clinic-add-ticket" }),
    new HtmlWebpackPlugin({ filename: "clinic-billing.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-billing.html", inject: true, hash: true, title: "clinic-billing" }),
    new HtmlWebpackPlugin({ filename: "clinic-blog-details.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-blog-details.html", inject: true, hash: true, title: "clinic-blog-details" }),
    new HtmlWebpackPlugin({ filename: "clinic-blogs.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-blogs.html", inject: true, hash: true, title: "clinic-blogs" }),
    new HtmlWebpackPlugin({ filename: "clinic-change-password.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-change-password.html", inject: true, hash: true, title: "clinic-change-password" }),

    new HtmlWebpackPlugin({ filename: "clinic-chat-call.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-chat-call.html", inject: true, hash: true, title: "clinic-chat-call" }),
    new HtmlWebpackPlugin({ filename: "clinic-contactus.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-contactus.html", inject: true, hash: true, title: "clinic-contactus" }),
    new HtmlWebpackPlugin({ filename: "clinic-dashboard.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-dashboard.html", inject: true, hash: true, title: "clinic-dashboard" }),
    new HtmlWebpackPlugin({ filename: "clinic-earning.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-earning.html", inject: true, hash: true, title: "clinic-earning" }),
    new HtmlWebpackPlugin({ filename: "clinic-forgot-password.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-forgot-password.html", inject: true, hash: true, title: "clinic-forgot-password" }),
    new HtmlWebpackPlugin({ filename: "clinic-help-center.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-help-center.html", inject: true, hash: true, title: "clinic-help-center" }),
    new HtmlWebpackPlugin({ filename: "clinic-inbox.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-inbox.html", inject: true, hash: true, title: "clinic-inbox" }),
    new HtmlWebpackPlugin({ filename: "clinic-login.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-login.html", inject: true, hash: true, title: "clinic-login" }),
    new HtmlWebpackPlugin({ filename: "clinic-myprofile.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-myprofile.html", inject: true, hash: true, title: "clinic-myprofile" }),
    new HtmlWebpackPlugin({ filename: "clinic-mysubscription.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-mysubscription.html", inject: true, hash: true, title: "clinic-mysubscription" }),

    new HtmlWebpackPlugin({ filename: "clinic-onboarding.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-onboarding.html", inject: true, hash: true, title: "clinic-onboarding" }),
    new HtmlWebpackPlugin({ filename: "clinic-pages.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-pages.html", inject: true, hash: true, title: "clinic-pages" }),
    new HtmlWebpackPlugin({ filename: "clinic-patients-documents.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-patients-documents.html", inject: true, hash: true, title: "clinic-patients-documents" }),
    new HtmlWebpackPlugin({ filename: "clinic-patients.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-patients.html", inject: true, hash: true, title: "clinic-patients" }),
    new HtmlWebpackPlugin({ filename: "clinic-personalization.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-personalization.html", inject: true, hash: true, title: "clinic-personalization" }),
    new HtmlWebpackPlugin({ filename: "clinic-profile.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-profile.html", inject: true, hash: true, title: "clinic-profile" }),
    new HtmlWebpackPlugin({ filename: "clinic-schedule-cards.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-schedule-cards.html", inject: true, hash: true, title: "clinic-schedule-cards" }),
    new HtmlWebpackPlugin({ filename: "clinic-schedule-grid.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-schedule-grid.html", inject: true, hash: true, title: "clinic-schedule-grid" }),
    new HtmlWebpackPlugin({ filename: "clinic-schedule-staff.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-schedule-staff.html", inject: true, hash: true, title: "clinic-schedule-staff" }),
    new HtmlWebpackPlugin({ filename: "clinic-schedule.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-schedule.html", inject: true, hash: true, title: "clinic-schedule" }),

    new HtmlWebpackPlugin({ filename: "clinic-settings-contact.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-settings-contact.html", inject: true, hash: true, title: "clinic-settings-contact" }),
    new HtmlWebpackPlugin({ filename: "clinic-settings-hospitals.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-settings-hospitals.html", inject: true, hash: true, title: "clinic-settings-hospitals" }),
    new HtmlWebpackPlugin({ filename: "clinic-settings-payment.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-settings-payment.html", inject: true, hash: true, title: "clinic-settings-payment" }),
    new HtmlWebpackPlugin({ filename: "clinic-settings-timing.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-settings-timing.html", inject: true, hash: true, title: "clinic-settings-timing" }),
    new HtmlWebpackPlugin({ filename: "clinic-settings-users.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-settings-users.html", inject: true, hash: true, title: "clinic-settings-users" }),
    new HtmlWebpackPlugin({ filename: "clinic-settings.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-settings.html", inject: true, hash: true, title: "clinic-settings" }),
    new HtmlWebpackPlugin({ filename: "clinic-signup-success.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-signup-success.html", inject: true, hash: true, title: "clinic-signup-success" }),
    new HtmlWebpackPlugin({ filename: "clinic-signup.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-signup.html", inject: true, hash: true, title: "clinic-signup" }),
    new HtmlWebpackPlugin({ filename: "clinic-staff-documents.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-staff-documents.html", inject: true, hash: true, title: "clinic-staff-documents" }),
    new HtmlWebpackPlugin({ filename: "clinic-statistics.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-statistics.html", inject: true, hash: true, title: "clinic-statistics" }),

    new HtmlWebpackPlugin({ filename: "clinic-subscriptions.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-subscriptions.html", inject: true, hash: true, title: "clinic-subscriptions" }),
    new HtmlWebpackPlugin({ filename: "clinic-ticket-list.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-ticket-list.html", inject: true, hash: true, title: "clinic-ticket-list" }),
    new HtmlWebpackPlugin({ filename: "clinic-users.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-users.html", inject: true, hash: true, title: "clinic-users" }),
    new HtmlWebpackPlugin({ filename: "clinic-view-patient.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/clinic-view-patient.html", inject: true, hash: true, title: "clinic-view-patient" }),

    // components    
    new HtmlWebpackPlugin({ filename: "components.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/components.html", inject: true, hash: true, title: "components" }),
    new HtmlWebpackPlugin({ filename: "component-accordions.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-accordions.html", inject: true, hash: true, title: "component-accordions" }),
    new HtmlWebpackPlugin({ filename: "component-alerts.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-alerts.html", inject: true, hash: true, title: "component-alerts" }),
    new HtmlWebpackPlugin({ filename: "component-avatar.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-avatar.html", inject: true, hash: true, title: "component-avatar" }),
    new HtmlWebpackPlugin({ filename: "component-badges.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-badges.html", inject: true, hash: true, title: "component-badges" }),
    new HtmlWebpackPlugin({ filename: "component-bootstrap-icons.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-bootstrap-icons.html", inject: true, hash: true, title: "component-bootstrap-icons" }),
    new HtmlWebpackPlugin({ filename: "component-bootstrap-icons.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-bootstrap-icons.html", inject: true, hash: true, title: "component-bootstrap-icons" }),
    new HtmlWebpackPlugin({ filename: "component-breadcrumbs.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-breadcrumbs.html", inject: true, hash: true, title: "component-breadcrumbs" }),
    new HtmlWebpackPlugin({ filename: "component-button-groups.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-button-groups.html", inject: true, hash: true, title: "component-button-groups" }),
    new HtmlWebpackPlugin({ filename: "component-buttons.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-buttons.html", inject: true, hash: true, title: "component-buttons" }),
    new HtmlWebpackPlugin({ filename: "component-cards.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-cards.html", inject: true, hash: true, title: "component-cards" }),
    new HtmlWebpackPlugin({ filename: "component-chartjs.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-chartjs.html", inject: true, hash: true, title: "component-chartjs" }),
    new HtmlWebpackPlugin({ filename: "component-checkboxes.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-checkboxes.html", inject: true, hash: true, title: "component-checkboxes" }),
    new HtmlWebpackPlugin({ filename: "component-collapse.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-collapse.html", inject: true, hash: true, title: "component-collapse" }),
    new HtmlWebpackPlugin({ filename: "component-colors.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-colors.html", inject: true, hash: true, title: "component-colors" }),
    new HtmlWebpackPlugin({ filename: "component-datatable.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-datatable.html", inject: true, hash: true, title: "component-datatable" }),
    new HtmlWebpackPlugin({ filename: "component-daterangepicker.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-daterangepicker.html", inject: true, hash: true, title: "component-daterangepicker" }),
    new HtmlWebpackPlugin({ filename: "component-dragula.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-dragula.html", inject: true, hash: true, title: "component-dragula" }),
    new HtmlWebpackPlugin({ filename: "component-dropdowns.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-dropdowns.html", inject: true, hash: true, title: "component-dropdowns" }),
    new HtmlWebpackPlugin({ filename: "component-dropzone.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-dropzone.html", inject: true, hash: true, title: "component-dropzone" }),
    new HtmlWebpackPlugin({ filename: "component-feather-icons.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-feather-icons.html", inject: true, hash: true, title: "component-feather-icons" }),
    new HtmlWebpackPlugin({ filename: "component-floating-label.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-floating-label.html", inject: true, hash: true, title: "component-floating-label" }),
    new HtmlWebpackPlugin({ filename: "component-full-calendar.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-full-calendar.html", inject: true, hash: true, title: "component-full-calendar" }),
    new HtmlWebpackPlugin({ filename: "component-header.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-header.html", inject: true, hash: true, title: "component-header" }),
    new HtmlWebpackPlugin({ filename: "component-heights-widths.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-heights-widths.html", inject: true, hash: true, title: "component-heights-widths" }),
    new HtmlWebpackPlugin({ filename: "component-icon-buttons.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-icon-buttons.html", inject: true, hash: true, title: "component-icon-buttons" }),
    new HtmlWebpackPlugin({ filename: "component-input-groups.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-input-groups.html", inject: true, hash: true, title: "component-input-groups" }),
    new HtmlWebpackPlugin({ filename: "component-inputs.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-inputs.html", inject: true, hash: true, title: "component-inputs" }),
    new HtmlWebpackPlugin({ filename: "component-list-groups.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-list-groups.html", inject: true, hash: true, title: "component-list-groups" }),
    new HtmlWebpackPlugin({ filename: "component-margin-padding.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-margin-padding.html", inject: true, hash: true, title: "component-margin-padding" }),
    new HtmlWebpackPlugin({ filename: "component-modal-dialogues.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-modal-dialogues.html", inject: true, hash: true, title: "component-modal-dialogues" }),
    new HtmlWebpackPlugin({ filename: "component-nav.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-nav.html", inject: true, hash: true, title: "component-nav" }),
    new HtmlWebpackPlugin({ filename: "component-off-canvas.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-off-canvas.html", inject: true, hash: true, title: "component-off-canvas" }),
    new HtmlWebpackPlugin({ filename: "component-pagination.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-pagination.html", inject: true, hash: true, title: "component-pagination" }),
    new HtmlWebpackPlugin({ filename: "component-popovers.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-popovers.html", inject: true, hash: true, title: "component-popovers" }),
    new HtmlWebpackPlugin({ filename: "component-pricing.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-pricing.html", inject: true, hash: true, title: "component-pricing" }),
    new HtmlWebpackPlugin({ filename: "component-progress.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-progress.html", inject: true, hash: true, title: "component-progress" }),
    new HtmlWebpackPlugin({ filename: "component-progressbar-js.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-progressbar-js.html", inject: true, hash: true, title: "component-progressbar-js" }),
    new HtmlWebpackPlugin({ filename: "component-radios.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-radios.html", inject: true, hash: true, title: "component-radios" }),
    new HtmlWebpackPlugin({ filename: "component-riskometer.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-riskometer.html", inject: true, hash: true, title: "component-riskometer" }),
    new HtmlWebpackPlugin({ filename: "component-scrollspy.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-scrollspy.html", inject: true, hash: true, title: "component-scrollspy" }),
    new HtmlWebpackPlugin({ filename: "component-selects.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-selects.html", inject: true, hash: true, title: "component-selects" }),
    new HtmlWebpackPlugin({ filename: "component-sidebars.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-sidebars.html", inject: true, hash: true, title: "component-sidebars" }),
    new HtmlWebpackPlugin({ filename: "component-sliders.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-sliders.html", inject: true, hash: true, title: "component-sliders" }),
    new HtmlWebpackPlugin({ filename: "component-smartwizard.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-smartwizard.html", inject: true, hash: true, title: "component-smartwizard" }),
    new HtmlWebpackPlugin({ filename: "component-spinners-loaders.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-spinners-loaders.html", inject: true, hash: true, title: "component-spinners-loaders" }),
    new HtmlWebpackPlugin({ filename: "component-swiper-carousel.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-swiper-carousel.html", inject: true, hash: true, title: "component-swiper-carousel" }),
    new HtmlWebpackPlugin({ filename: "component-switches.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-switches.html", inject: true, hash: true, title: "component-switches" }),
    new HtmlWebpackPlugin({ filename: "component-tables.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-tables.html", inject: true, hash: true, title: "component-tables" }),
    new HtmlWebpackPlugin({ filename: "component-tabs.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-tabs.html", inject: true, hash: true, title: "component-tabs" }),
    new HtmlWebpackPlugin({ filename: "component-toasts.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-toasts.html", inject: true, hash: true, title: "component-toasts" }),
    new HtmlWebpackPlugin({ filename: "component-tooltips.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-tooltips.html", inject: true, hash: true, title: "component-tooltips" }),
    new HtmlWebpackPlugin({ filename: "component-validation.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/component-validation.html", inject: true, hash: true, title: "component-validation" }),

    // documentation
    new HtmlWebpackPlugin({ filename: "documentation.html", template: "!!html-webpack-plugin/lib/loader.js!./src/pages/documentation.html", inject: true, title: "Document" }),
  ],
  module: {
    rules: [
      // Babel-loader
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        use: {
          loader: "babel-loader",
          options: {
            cacheDirectory: true
          }
        }
      },
      // Css-loader & sass-loader
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          "postcss-loader",
          "sass-loader"
        ]
      },

      // Load fonts
      {
        test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
        type: "asset/resource",
        generator: {
          filename: "assets/fonts/[name][ext]"
        }
      },

      // Load images
      {
        test: /\.(png|jpg|jpeg|gif)(\?v=\d+\.\d+\.\d+)?$/,
        type: "asset/resource",
        generator: {
          filename: "assets/img/[name][ext]"
        }
      },

      {
        test: /\.html$/,
        exclude: /(node_modules)/,
        use: {
          loader: "html-loader",
          options: {
            sources: false,
          }
        }
      },
    ]
  },
  resolve: {
    extensions: [".js", ".scss"],
    modules: ["node_modules"],
    alias: {
      request$: "xhr"
    }
  },
  devServer: {
    static: {
      directory: Path.join(__dirname, "dist")
    },
    port: 8080,
    open: true,
  }
};
