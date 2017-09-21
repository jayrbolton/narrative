/*jslint white: true*/
/*global module */
module.exports = function (config) {
    'use strict';
    config.set({
        basePath: '../../',
        frameworks: ['jasmine', 'requirejs'],
        plugins: [
            'karma-jasmine',
            // 'karma-chrome-launcher',
            'karma-phantomjs-launcher',
            'karma-coverage',
            'karma-requirejs'
        ],
        preprocessors: {
            'kbase-extension/static/kbase/**/*.js': ['coverage']
        },
        files: [
            // {pattern: 'kbase-extension/static/components/**/*.js', included: false},
            // {pattern: 'kbase-extension/static/kbase/js/*.js', included: false},
            // {pattern: 'kbase-extension/static/kbase/js/widgets/**/*.js', included: false},
            // {pattern: 'kbase-extension/static/**/*.json', included: false},

            {pattern: 'test/unit/spec/**/*.js', included: false},
            'kbase-extension/static/narrative_paths.js',
            {pattern: 'test/unit/testConfig.json', included: false, served: true, nocache: true},
            {pattern: 'test/*.tok', included: false, served: true, nocache: true},
            'test/unit/testUtil.js',
            'test/unit/test-main.js'
        ],
        // test results reporter to use
        // possible values: 'dots', 'progress'
        // available reporters: https://npmjs.org/browse/keyword/karma-reporter
        reporters: ['progress', 'coverage'],
        coverageReporter: {
            type: 'html',
            dir: 'js-coverage/'
        },
        // web server port
        port: 9876,
        // enable / disable colors in the output (reporters and logs)
        colors: true,
        // level of logging
        // possible values: config.LOG_DISABLE || config.LOG_ERROR || config.LOG_WARN || config.LOG_INFO || config.LOG_DEBUG
        logLevel: config.LOG_INFO,
        // enable / disable watching file and executing tests whenever any file changes
        autoWatch: false,
        // start these browsers
        // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
        browsers: ['PhantomJS'],
        // Continuous Integration mode
        // if true, Karma captures browsers, runs the tests and exits
        // phantomjsLauncher: {
        //     options: {
        //         settings: {
        //             webSecurityEnabled: false
        //         }
        //     }
        // },
        singleRun: true,
        proxies: {
            '/narrative/static/': 'http://localhost:9999/narrative/static/',
            '/static/': 'http://localhost:9999/narrative/static/',
            '/test/': '/base/test/'
        }

    });
};
