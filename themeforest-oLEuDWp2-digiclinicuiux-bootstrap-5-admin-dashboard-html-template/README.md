# Product of Adminuiux - Quickstarter

### Build tools

The theme includes a custom Webpack file, which can be used to quickly recompile and minify theme assets while developing or for deployment. You'll need to install Node.js before using Webpack.

Once Node.js is installed, run npm install to install the rest of Adminuiux's dependencies. All dependencies will be downloaded to the node_modules directory.

```sh
npm install
```

Now you're ready to modify the source files and generate new dist/ files. Adminuiux uses webpack-dev-server to automatically detect file changes and start a local webserver at http://localhost:8080.

```sh
npm start
```

Compile, optimize, minify and uglify all source files to dist/ folder:

```sh
npm run build
```

Read more at :hostURL(dist folder) / documentation.html
