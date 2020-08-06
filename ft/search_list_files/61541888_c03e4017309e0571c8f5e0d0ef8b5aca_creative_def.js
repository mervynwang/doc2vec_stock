(function() {
  var creativeDefinition = {
    customScriptUrl: '',
    isDynamic: false,
    delayedImpression: false,
    standardEventIds: {
      DISPLAY_TIMER: '72',
      INTERACTION_TIMER: '73',
      INTERACTIVE_IMPRESSION: '74',
      MANUAL_CLOSE: '75',
      BACKUP_IMAGE_IMPRESSION: '76',
      EXPAND_TIMER: '77',
      FULL_SCREEN: '78',
      VIDEO_PLAY: '79',
      VIDEO_VIEW_TIMER: '80',
      VIDEO_COMPLETE: '81',
      VIDEO_INTERACTION: '82',
      VIDEO_PAUSE: '83',
      VIDEO_MUTE: '84',
      VIDEO_REPLAY: '85',
      VIDEO_MIDPOINT: '86',
      VIDEO_STOP: '87',
      VIDEO_UNMUTE: '88',
      DYNAMIC_CREATIVE_IMPRESSION: '',
      HTML5_CREATIVE_IMPRESSION: ''
    },
    exitEvents: [
      {
        name: 'Default Exit',
        reportingId: '40669249',
        url: '',
        targetWindow: '_blank',
        windowProperties: ''
      },
      {
        name: 'Hub Exit',
        reportingId: '40671889',
        url: '',
        targetWindow: '_blank',
        windowProperties: ''
      },
      {
        name: 'article1',
        reportingId: '41701249',
        url: 'https://www.ft.com/content/7d940587-4502-4468-acea-a67b7bf6a523',
        targetWindow: '_blank',
        windowProperties: ''
      },
      {
        name: 'article2',
        reportingId: '41701489',
        url: 'https://www.ft.com/content/b4a112dd-cafd-4522-bf79-9e25704577ab',
        targetWindow: '_blank',
        windowProperties: ''
      },
      {
        name: 'article3',
        reportingId: '41701729',
        url: 'https://www.ft.com/content/4f807d17-2f95-4572-a7f4-50655fdda00e',
        targetWindow: '_blank',
        windowProperties: ''
      },
      {
        name: 'article4',
        reportingId: '41701969',
        url: 'https://www.ft.com/content/100f0c5b-83c5-4e9a-8ad0-89af2ea4a758',
        targetWindow: '_blank',
        windowProperties: ''
      },
      {
        name: 'article5',
        reportingId: '41702209',
        url: 'https://www.ft.com/content/6f6b60b3-9dd3-42c3-a5e7-6cf61863759b',
        targetWindow: '_blank',
        windowProperties: ''
      },
      {
        name: 'article6',
        reportingId: '41702449',
        url: 'https://www.ft.com/content/5e0d475f-f8d0-4f86-873b-97e9ec5504f0',
        targetWindow: '_blank',
        windowProperties: ''
      }
    ],
    timerEvents: [
    ],
    counterEvents: [
    ],
    childFiles: [
      {
        name: 'static-970-250.png',
        url: '/ads/richmedia/studio/pv2/61520911/20200803100556119/static-970-250.png',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'ft-suite.js',
        url: '/ads/richmedia/studio/pv2/61520911/20200803100556119/ft-suite.js',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'nav-button.svg',
        url: '/ads/richmedia/studio/pv2/61520911/20200803100556119/nav-button.svg',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'wemeanbusinesscoalition.png',
        url: '/ads/richmedia/studio/pv2/61520911/20200803100556119/wemeanbusinesscoalition.png',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'billboard-970-250.css',
        url: '/ads/richmedia/studio/pv2/61520911/20200803100556119/billboard-970-250.css',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'data.js',
        url: '/ads/richmedia/studio/pv2/61520911/20200803100556119/data.js',
        isVideo: false,
        transcodeInformation: null
      },
      {
        name: 'vendor.js',
        url: '/ads/richmedia/studio/pv2/61520911/20200803100556119/vendor.js',
        isVideo: false,
        transcodeInformation: null
      }
    ],
    videoFiles: [
    ],
    videoEntries: [
    ],
    primaryAssets: [
      {
        id: '80812550',
        artworkType: 'HTML5',
        displayType: 'BANNER',
        width: '970',
        height: '250',
        servingPath: '/ads/richmedia/studio/pv2/61520911/20200803100556119/billboard-970-250.html',
        zIndex: '1000000',
        customCss: '',
        flashArtworkTypeData: null,
        htmlArtworkTypeData: {
          isTransparent: false,
          sdkVersion: '01_244' // Duplicating sdk version in subsequent field as version format not the same.
        },
        floatingDisplayTypeData: null,
        expandingDisplayTypeData: null,
        imageGalleryTypeData: null,
        pageSettings:null,
layoutsConfig: null,
layoutsApi: null
      }
    ]
  }
  var rendererDisplayType = '';
  rendererDisplayType += 'html_';
  var rendererFormat = 'inpage';
  var rendererName = rendererDisplayType + rendererFormat;

  var creativeId = '138319203412';
  var adId = '0';
  var templateVersion = '200_260';
  var studioObjects = window['studioV2'] = window['studioV2'] || {};
  var creativeObjects = studioObjects['creatives'] = studioObjects['creatives'] || {};
  var creativeKey = [creativeId, adId].join('_');
  var creative = creativeObjects[creativeKey] = creativeObjects[creativeKey] || {};
  creative['creativeDefinition'] = creativeDefinition;
  var adResponses = creative['adResponses'] || [];
  for (var i = 0; i < adResponses.length; i++) {
    adResponses[i].creativeDto && adResponses[i].creativeDto.csiEvents &&
        (adResponses[i].creativeDto.csiEvents['pe'] =
            adResponses[i].creativeDto.csiEvents['pe'] || (+new Date));
  }
  var loadedLibraries = studioObjects['loadedLibraries'] = studioObjects['loadedLibraries'] || {};
  var versionedLibrary = loadedLibraries[templateVersion] = loadedLibraries[templateVersion] || {};
  var typedLibrary = versionedLibrary[rendererName] = versionedLibrary[rendererName] || {};
  if (typedLibrary['bootstrap']) {
    typedLibrary.bootstrap();
  }
})();
