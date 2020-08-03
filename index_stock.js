var request = require('request');
var requestOptions = {
    'url': 'https://api.tiingo.com/tiingo/daily/biib/prices?token=f3c2e60b7910a04405520e045ebcd23e444bd76a&startDate=2000-01-01',
    'headers': {
        'Content-Type': 'application/json'
        }
};

request(requestOptions,
    function(error, response, body) {
        console.log(body);
    }
);        
    
