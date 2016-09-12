Name:  Mounika Akuthota

Ip address:http://104.131.191.152

Link to phpmyadmin: http://104.131.191.152/phpmyadmin

#gift_options.sql
```
CREATE TABLE IF NOT EXISTS `gift_options` (
  `itemId` int(64) NOT NULL DEFAULT '0',
  `allowGiftWrap` tinyint(1) NOT NULL,
  `allowGiftMessage` tinyint(1) NOT NULL,
  `allowGiftReceipt` tinyint(1) NOT NULL,
  PRIMARY KEY (`itemId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

```
#image_entities.sql
```
CREATE TABLE IF NOT EXISTS `image_entities` (
  `itemId` int(64) NOT NULL,
  `thumbnailImage` varchar(32) NOT NULL,
  `mediumImage` varchar(32) NOT NULL,
  `largeImage` varchar(32) NOT NULL,
  `entityType` tinytext NOT NULL,
  PRIMARY KEY (`itemId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

```
#market_place_price.sql
```
CREATE TABLE IF NOT EXISTS `market_place_price` (
  `itemId` int(64) NOT NULL,
  `price` float(6,6) NOT NULL,
  `sellerInfo` tinytext NOT NULL,
  `standardShipRate` int(8) NOT NULL,
  `twoThreeDayShippingRate` float(4,2) NOT NULL,
  `availableOnline` tinyint(1) NOT NULL,
  `clearance` tinyint(1) NOT NULL,
  `offerType` varchar(32) NOT NULL,
  PRIMARY KEY (`itemId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

```
#products.sql
```
CREATE TABLE IF NOT EXISTS `products` (
  `itemId` int(64) NOT NULL,
  `parentItemId` int(32) NOT NULL,
  `name` varchar(64) NOT NULL,
  `salePrice` float(6,2) NOT NULL,
  `upc` int(64) NOT NULL,
  `categoryPath` varchar(64) NOT NULL,
  `shortDescription` varchar(128) NOT NULL,
  `longDescription` varchar(128) NOT NULL,
  `brandName` varchar(8) NOT NULL,
  `thumbnailImage` varchar(128) NOT NULL,
  `mediumImage` varchar(128) NOT NULL,
  `largeImage` varchar(128) NOT NULL,
  `productTrackingUrl` varchar(128) NOT NULL,
  `modelNumber` varchar(8) NOT NULL,
  `productUrl` varchar(32) NOT NULL,
  `categoryNode` varchar(32) NOT NULL,
  `stock` tinytext NOT NULL,
  `addToCartUrl` varchar(64) NOT NULL,
  `affiliateAddToCartUrl` varchar(64) NOT NULL,
  `offerType` varchar(32) NOT NULL,
  `msrp` float(6,2) NOT NULL,
  `standardShipRate` float(4,2) NOT NULL,
  `color` tinytext NOT NULL,
  `customerRating` float(4,3) NOT NULL,
  `numReviews` int(8) NOT NULL,
  `customerRatingImage` varchar(32) NOT NULL,
  `maxItemsInOrder` int(8) NOT NULL,
  `size` varchar(8) NOT NULL,
  `sellerInfo` tinytext NOT NULL,
  `age` varchar(32) NOT NULL,
  `gender` tinytext NOT NULL,
  `isbn` int(32) NOT NULL,
  `preOrderShipsOn` varchar(32) NOT NULL,
  PRIMARY KEY (`itemId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
```
