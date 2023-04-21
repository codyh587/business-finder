import React from 'react'
import { Link } from 'react-router-dom'

const ValidTypes = () => {
    const type_identifiers = {
        'EatDrink': [
            'Bars', 'BarsGrillsAndPubs', 'BelgianRestaurants',
            'BreweriesAndBrewPubs', 'BritishRestaurants', 'BuffetRestaurants',
            'CafeRestaurants', 'CaribbeanRestaurants', 'ChineseRestaurants',
            'CocktailLounges', 'CoffeeAndTea', 'Delicatessens', 'DeliveryService',
            'Diners', 'DiscountStores', 'Donuts', 'FastFood', 'FrenchRestaurants',
            'FrozenYogurt', 'GermanRestaurants', 'GreekRestaurants', 'Grocers',
            'Grocery', 'HawaiianRestaurants', 'HungarianRestaurants',
            'IceCreamAndFrozenDesserts', 'IndianRestaurants', 'ItalianRestaurants',
            'JapaneseRestaurants', 'Juices', 'KoreanRestaurants', 'LiquorStores',
            'MexicanRestaurants', 'MiddleEasternRestaurants', 'Pizza',
            'PolishRestaurants', 'PortugueseRestaurants', 'Pretzels',
            'Restaurants', 'RussianAndUkrainianRestaurants', 'Sandwiches',
            'SeafoodRestaurants', 'SpanishRestaurants', 'SportsBars',
            'SteakHouseRestaurants', 'Supermarkets', 'SushiRestaurants',
            'TakeAway', 'Taverns', 'ThaiRestaurants', 'TurkishRestaurants',
            'VegetarianAndVeganRestaurants', 'VietnameseRestaurants'
        ],
        'SeeDo': [
            'AmusementParks', 'Attractions', 'Carnivals', 'Casinos',
            'LandmarksAndHistoricalSites', 'MiniatureGolfCourses', 'MovieTheaters',
            'Museums', 'Parks', 'SightseeingTours', 'TouristInformation', 'Zoos'
        ],
        'Shop': [
            'AntiqueStores', 'Bookstores', 'CDAndRecordStores',
            'ChildrensClothingStores', 'CigarAndTobaccoShops', 'ComicBookStores',
            'DepartmentStores', 'DiscountStores', 'FleaMarketsAndBazaars',
            'FurnitureStores', 'HomeImprovementStores', 'JewelryAndWatchesStores',
            'KitchenwareStores', 'LiquorStores', 'MallsAndShoppingCenters',
            'MensClothingStores', 'MusicStores', 'OutletStores', 'PetShops',
            'PetSupplyStores', 'SchoolAndOfficeSupplyStores', 'ShoeStores',
            'SportingGoodsStores', 'ToyAndGameStores',
            'VitaminAndSupplementStores', 'WomensClothingStores'
        ],
        'BanksAndCreditUnions': [],
        'Hospitals': [],
        'HotelsAndMotels': [],
        'Parking': []
    };

    return (
        <div className="ValidTypes">
            <div className='grid grid-cols-1 gap-10 pt-10 pb-10'>
                <h1 className="card-title justify-center">Valid Business Types</h1>
                <div className='grid grid-cols-2 gap-3'>
                    {
                        Object.keys(type_identifiers).map(
                            (mainType) => (
                                <div className="card card-compact w-96 h-fit shadow-xl">
                                    <div className="card-body">
                                        <h2 className="card-title">"{mainType}"</h2>
                                        <p>{type_identifiers[mainType].join(", ")}</p>
                                    </div>
                                </div>
                            )
                        )
                    }
                    <button className="btn h-full"><Link to={`/`}>Back</Link></button>
                </div>
            </div>
        </div>
    );
};

export default ValidTypes
