'use strict';

angular.module('shopstatsApp.version', [
  'shopstatsApp.version.interpolate-filter',
  'shopstatsApp.version.version-directive'
])

.value('version', '0.1');
