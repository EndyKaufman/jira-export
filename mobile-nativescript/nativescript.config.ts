import { NativeScriptConfig } from '@nativescript/cli';

export default {
  id: 'ru.site15.jira-export',
  appResourcesPath: 'App_Resources',
  android: {
    v8Flags: '--expose_gc',
    markingMode: 'none'
  }
} as NativeScriptConfig;