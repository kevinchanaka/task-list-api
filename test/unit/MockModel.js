// Library to mock models for unit testing

function makeMockModel() {
  let dataArray = [];
  return Object.freeze({
    insert,
    findAll,
    findById,
    remove,
    update,
    destroy,
  });

  async function findAll() {
    return dataArray;
  }

  async function insert(data) {
    dataArray.push(data);
  }

  async function findById(id) {
    return dataArray.filter((value) => value.id == id)[0];
  }

  async function remove(id) {
    dataArray = dataArray.filter((value) => value.id != id);
  }

  async function update(data) {
    dataArray = dataArray.map((value) => {
      if (data.id == value.id) {
        return data;
      }
      return value;
    });
  }

  async function destroy() {
    dataArray = [];
  }
}

module.exports = {makeMockModel};
