const gulp = require('gulp');
const eslint = require('gulp-eslint');

gulp.task('lint', () => gulp.src(['**/*.{js,jsx}', '!node_modules/**'])
  .pipe(eslint())
  .pipe(eslint.format())
  .pipe(eslint.failAfterError()));

gulp.task('watch', () => {
  gulp.watch('**/*.{js,jsx}', ['lint']);
});

gulp.task('default', ['watch'], () => {
});
