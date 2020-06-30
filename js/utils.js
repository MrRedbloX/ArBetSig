class Utils{
  static chunks(array, size) {
    return Array.apply(0,{length: Math.ceil(array.length / size)}).map((_, index) => array.slice(index*size, (index+1)*size))
  }
}

module.exports = Utils
