document.addEventListener('DOMContentLoaded', function () {
    const table = $('#expenses-table').DataTable();

    $('#expense-search').on('keyup', function () {
      table.search(this.value).draw();
    });
  });