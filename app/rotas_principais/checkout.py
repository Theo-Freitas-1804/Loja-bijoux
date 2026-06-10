from datetime import date

from flask import (
    Blueprint,
    render_template,
    current_app,
    flash,
    request,
    session,
    redirect,
    url_for
)

from flask_login import (
    current_user,
    login_required
)

from ..models import (
    db,
    Produtos,
    Carrinho,
    Usuario,
    Cupom,
    Pedido,
    Itens,
    status_acessorio
)

from ..rota_perfil.cupons import validar_cupom_checkout
from ..services.frete import calcular_frete


bp_checkout = Blueprint(
    "checkout",
    __name__
)


def criar_pedido(
    usuario,
    subtotal,
    total_final,
    envio,
    data_entrega
):

    pedido = Pedido(
        usuaria=usuario.id_usuaria,
        total=total_final,
        status="Pendente",
        envio=envio,
        data_entrega=data_entrega
    )

    db.session.add(pedido)
    db.session.flush()

    return pedido

def criar_itens_pedido(
    pedido,
    itens_carrinho
):
  for item in itens_carrinho:

      produto = Produtos.query.get(
          item.produto_id
      )

      if not produto:
          continue

      novo_item = Itens(
          pedido_id=pedido.id,
          produto_id=item.produto_id,
          quantidade=item.quantidade,
          preco_unit=produto.preco
      )

      db.session.add(novo_item)

      # ESTOQUE

      produto.em_estoque -= (
          item.quantidade
      )

      if produto.em_estoque <= 0:

          produto.em_estoque = 0

          produto.status = (
              status_acessorio.VENDIDO
          )

def limpar_carrinho(usuario_id):

    Carrinho.query.filter_by(
        usuario_id=usuario_id
    ).delete()


@bp_checkout.route("/checkout")
@login_required
def checkout():

    itens = Carrinho.query.filter_by(
        usuario_id=current_user.id_usuaria
    ).all()

    produtos_checkout = []
    subtotal = 0

    for item in itens:

        produto = Produtos.query.get(
            item.produto_id
        )

        if produto:

            produtos_checkout.append({
                "produto": produto,
                "quantidade": item.quantidade,
                "subtotal": produto.preco * item.quantidade
            })

            subtotal += (
                produto.preco *
                item.quantidade
            )

    cupom_id = session.get("cupom_id")

    cupom_valido = None
    desconto = 0
    valor_com_desconto = subtotal

    if cupom_id:

        cupom = Cupom.query.filter_by(
            id_cupom=cupom_id
        ).first()

        cupom_valido = aplicar_cupom()

        if cupom_valido:

            if cupom.tipo == "fixo":

                desconto = (
                    cupom.valor_desconto
                )

            elif cupom.tipo == "porcentagem":

                desconto = (
                    float(subtotal) *
                    (
                        cupom.valor_desconto
                        / 100
                    )
                )

            valor_com_desconto = (
                float(subtotal)
                - desconto
            )

    end = current_user.enderecos[0]

    fretes = calcular_frete(end)

    return render_template(
        "checkout.html",
        produtos_checkout=produtos_checkout,
        enderecos=current_user.enderecos,
        subtotal=subtotal,
        desconto=desconto,
        valor_com_desconto=valor_com_desconto,
        cupom_aplicado=cupom_valido,
        cupons=current_user.cupons,
        fretes=fretes
    )


@bp_checkout.route(
    "/finalizar-compra",
    methods=["POST"]
)
@login_required
def finalizar_compra():
  itens_carrinho = Carrinho.query.filter_by(
    usuario_id=current_user.id_usuaria
    ).all()
    # Verifica estoque ANTES
  for item in itens_carrinho:
    produto = Produtos.query.get(
      item.produto_id
    )
    if not produto:
      continue
    if produto.em_estoque < item.quantidade:
        flash(
            f"{produto.nome} não possui estoque suficiente."
        )
        return redirect(
            url_for(
                "checkout.checkout"
            )
        )
  if not itens_carrinho:
      flash(
          "Carrinho vazio"
      )
      return redirect(
          url_for(
              "checkout.checkout"
          )
      )
  
  subtotal = 0
  
  for item in itens_carrinho:
  
      produto = Produtos.query.get(
          item.produto_id
      )
  
      if produto:
  
          subtotal += (
              produto.preco *
              item.quantidade
          )
  
  # TEMPORÁRIO
  total_final = subtotal
  
  pedido = criar_pedido(
      usuario=current_user,
      subtotal=subtotal,
      total_final=total_final,
      envio="sexta",
      data_entrega=date.today()
  )
  
  criar_itens_pedido(
      pedido,
      itens_carrinho
  )
  
  limpar_carrinho(
      current_user.id_usuaria
  )
  
  produto.em_estoque -= item.quantidade
  if produto.em_estoque <= 0:
    produto.status = status_acessorio.VENDIDO
  
  db.session.commit()
  
  flash(
      "Compra finalizada. Redirecionando..."
  )
  
  return redirect(
      url_for(
          "usuario.perfil"
      )
  )