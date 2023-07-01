function ensSil(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Başlıklı botu silmek istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Sil !'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}

function ensDuzenle(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Başlıklı botu düzenlemek istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Düzenle !'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}

function ensAktif(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Başlıklı botu aktif yapmak istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Aktif Yap!'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}

function ensPasif(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Başlıklı botu pasif yapmak istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Pasif Yap!'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}


function catSil(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Başlıklı kategoriyi silmek istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Sil !'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}

function catDuzenle(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Başlıklı kategoriyi düzenlemek istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Düzenle !'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}

function userDuzenle(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Kullanıcıyı düzenlemek istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Düzenle !'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}

function userSil(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Kullanıcıyı silmek istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Sil !'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}

function userAdminYap(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Kullanıcıyı admin yapmak istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Admin Yap !'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}

function userUyeYap(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Kullanıcıyı üye yapmak istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Üye Yap !'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
    setTimeout(function(){location.reload();}, 3000); // 3 saniye sonra sayfayı yenile
  }
  })
}

function pacSil(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Başlıklı paketi silmek istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Sil !'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}

function pacDuzenle(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Başlıklı paketi düzenlemek istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Düzenle !'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}

function pacAktif(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Başlıklı paketi aktif yapmak istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Aktif Yap!'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}

function pacPasif(url,title){

    Swal.fire({
  title: '! Dikkat !',
  text: `${title} Başlıklı paketi pasif yapmak istediğinize eminmisiniz ?`,
  icon: 'warning',
  showCancelButton: true,
  confirmButtonColor: '#3085d6',
  cancelButtonColor: '#d33',
  confirmButtonText: 'Eminim Pasif Yap!'
  }).then((result) => {
  if (result.isConfirmed) {
    location.href=url
  }
  })
}
