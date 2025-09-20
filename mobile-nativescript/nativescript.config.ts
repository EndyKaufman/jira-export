import { NativeScriptConfig } from '@nativescript/cli';

export default {
  id: 'org.nativescript.hello',
  appResourcesPath: 'App_Resources',
  android: {
    v8Flags: '--expose_gc',
    markingMode: 'none'
  }
} as NativeScriptConfig;