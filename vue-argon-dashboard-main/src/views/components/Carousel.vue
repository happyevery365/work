<template>
  <div class="card card-carousel overflow-hidden h-100 p-0">
    <div
      id="carouselExampleCaptions"
      class="carousel slide h-100"
      data-bs-ride="carousel"
    >
      <div class="carousel-inner border-radius-lg h-100">
        <div
          class="carousel-item h-100 active"
          :style="{
            backgroundImage:
              'url(' + require('@/assets/img/carousel-1.jpg') + ')',
            backgroundSize: 'cover',
          }"
        >
          <div
            class="carousel-caption d-none d-md-block bottom-0 text-start start-0 ms-5"
          >
            <h5 class="text-white mb-1">开始搜索吧！</h5>
            <p>
              您可以在搜索页面搜索商品，查看不同平台的价格~
            </p>
          </div>
        </div>
        <div
          class="carousel-item h-100"
          :style="{
            backgroundImage:
              'url(' + require('@/assets/img/carousel-2.jpg') + ')',
            backgroundSize: 'cover',
          }"
        >
          <div
            class="carousel-caption d-none d-md-block bottom-0 text-start start-0 ms-5"
          >

            <h5 class="text-white mb-1">收藏喜欢的商品！</h5>
            <p>
              您可以点击图片打开您喜欢的商品，并收藏它，在收藏页面查看收藏的商品~
            </p>
          </div>
        </div>
        <div
          class="carousel-item h-100"
          :style="{
            backgroundImage:
              'url(' + require('@/assets/img/carousel-3.jpg') + ')',
            backgroundSize: 'cover',
          }"
        >
          <div
            class="carousel-caption d-none d-md-block bottom-0 text-start start-0 ms-5"
          >
            <h5 class="text-white mb-1">关于降价提醒</h5>
            <p>
              每日我们会对您收藏的商品进行实时价格查寻，并将降价信息发送至您的邮箱。您也可以在我的页面查看~
            </p>
          </div>
        </div>
      </div>
      <button
        class="carousel-control-prev w-5 me-3"
        type="button"
        data-bs-target="#carouselExampleCaptions"
        data-bs-slide="prev"
      >
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button
        class="carousel-control-next w-5 me-3"
        type="button"
        data-bs-target="#carouselExampleCaptions"
        data-bs-slide="next"
      >
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
  </div>
</template>
