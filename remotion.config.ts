import {Config} from '@remotion/cli/config';

Config.setEntryPoint('src/index.ts');
Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(92);
Config.setCodec('h264');
Config.setCrf(19);
Config.setColorSpace('bt709');
Config.setPixelFormat('yuv420p');
Config.setAudioCodec('aac');
Config.setAudioBitrate('256k');
Config.setConcurrency('100%');
// Measured in a 4-vCPU cloud container: 'angle' renders ~8x faster than 'swangle' with identical output.
Config.setChromiumOpenGlRenderer('angle');
