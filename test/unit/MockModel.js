// Library to mock models for unit testing

export function makeMockModel() {
  let dataArray = [];
  return Object.freeze({
    insert,
    findAllByField,
    findByField,
    removeByField,
    update,
    destroy,
  });

  async function insert(data) {
    dataArray.push(data);
  }

  async function update(data) {
    dataArray = dataArray.map((value) => {
      if (data.id == value.id) {
        return data;
      }
      return value;
    });
  }

  async function findByField(obj) {
    return dataArray.filter((value) => isSubset(obj, value))[0];
  }

  async function findAllByField(obj) {
    return dataArray.filter((value) => isSubset(obj, value));
  }

  async function removeByField(obj) {
    dataArray = dataArray.filter((value) => !isSubset(obj, value));
  }

  function isSubset(obj1, obj2) {
    let numEqual = 0;
    for (const [k1, v1] of Object.keys(obj1)) {
      for (const [k2, v2] of Object.keys(obj2)) {
        if (k1 == k2 && v1 == v2) {
          numEqual = numEqual + 1;
        }
      }
    }
    return numEqual == Object.keys(obj1).length;
  }

  async function destroy() {
    dataArray = [];
  }
}
