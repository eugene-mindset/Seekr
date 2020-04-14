class ItemTags {
  static NONE = {label: null,             value: 0};
  static TECH = {label: 'tech',           value: 1};
  static CLOTHING = {label: 'clothing',   value: 2};
  static JEWELRY = {label: 'jewelry',     value: 4};
  static PET = {label: 'pet',             value: 8};
  static PERSONAL = {label: 'personal',   value: 16};
  static APPAREL = {label: 'apparel',     value: 32};
  static OTHER = {label: 'other',         value: 64};

  static StringTags = [
    "tech",
    "clothing",
    "jewelry",
    "pet",
    "personal",
    "apparel",
    "other"
  ];

  static getMapping() {
      return [this.TECH, this.CLOTHING, this.JEWELRY, this.PET, this.PERSONAL, this.APPAREL, this.OTHER];
  }

  static getStrings(val) {
    if (val === 0) {
        return '';
    }

    var maps = this.getMapping();
    var result = '';

    for (var tag in maps) {
        if ((val & maps[tag].value) === maps[tag].value) {
            result = result + maps[tag].label + ','
        }
    }

    return result.substring(0, result.length - 1);
  }
}

export default ItemTags;